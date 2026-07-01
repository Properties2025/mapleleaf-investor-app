from __future__ import annotations
from datetime import datetime, timezone
from typing import Any
import pandas as pd
from .sample_data import DEFAULT_MOCK, MOCK_TICKERS
from .storage import cache_snapshot, read_cached_snapshot

CACHE_MAX_AGE_HOURS = 12

def _safe_float(value: Any) -> float | None:
    try:
        if value is None or pd.isna(value):
            return None
        return float(value)
    except Exception:
        return None

def _pct_change_from_series(close: pd.Series, periods_back: int) -> float | None:
    if close is None or close.empty or len(close) <= periods_back:
        return None
    latest = _safe_float(close.iloc[-1])
    previous = _safe_float(close.iloc[-periods_back])
    if latest is None or previous in (None, 0):
        return None
    return round(((latest / previous) - 1) * 100, 2)

def _infer_market(ticker: str, currency: str | None) -> str:
    if ticker.upper().endswith(".TO") or currency == "CAD":
        return "Canada"
    if currency == "USD":
        return "U.S."
    return "Unknown"

def _history_to_records(history: pd.DataFrame) -> list[dict[str, Any]]:
    if history is None or history.empty or "Close" not in history.columns:
        return []
    out = history.reset_index()
    date_col = "Date" if "Date" in out.columns else out.columns[0]
    return [
        {"date": str(row[date_col])[:10], "close": _safe_float(row["Close"])}
        for _, row in out.tail(260).iterrows()
        if _safe_float(row["Close"]) is not None
    ]

def _load_yfinance_snapshot(ticker: str) -> dict[str, Any]:
    import yfinance as yf
    symbol = ticker.upper().strip()
    yf_ticker = yf.Ticker(symbol)
    history = yf_ticker.history(period="1y", interval="1d", auto_adjust=False)
    if history is None or history.empty:
        raise ValueError(f"No price history returned for {symbol}")
    close = history["Close"].dropna()
    current_price = _safe_float(close.iloc[-1]) if not close.empty else None
    info, fast_info = {}, {}
    try:
        info = yf_ticker.info or {}
    except Exception:
        pass
    try:
        fast_info = dict(yf_ticker.fast_info or {})
    except Exception:
        pass
    currency = info.get("currency") or fast_info.get("currency") or "USD"
    return {
        "ticker": symbol,
        "company_name": info.get("longName") or info.get("shortName") or symbol,
        "market": _infer_market(symbol, currency),
        "sector": info.get("sector") or "Unknown",
        "industry": info.get("industry") or "Unknown",
        "current_price": current_price or _safe_float(fast_info.get("last_price")),
        "currency": currency,
        "daily_change_pct": _pct_change_from_series(close, 2),
        "two_week_trend_pct": _pct_change_from_series(close, 10),
        "three_month_trend_pct": _pct_change_from_series(close, 63),
        "one_year_trend_pct": _pct_change_from_series(close, min(252, max(len(close)-1, 1))),
        "market_cap": _safe_float(info.get("marketCap") or fast_info.get("market_cap")),
        "trailing_pe": _safe_float(info.get("trailingPE")),
        "forward_pe": _safe_float(info.get("forwardPE")),
        "price_to_sales": _safe_float(info.get("priceToSalesTrailing12Months")),
        "revenue_growth": _safe_float(info.get("revenueGrowth")),
        "earnings_growth": _safe_float(info.get("earningsGrowth")),
        "profit_margins": _safe_float(info.get("profitMargins")),
        "debt_to_equity": _safe_float(info.get("debtToEquity")),
        "free_cashflow": _safe_float(info.get("freeCashflow")),
        "total_cash": _safe_float(info.get("totalCash")),
        "history": _history_to_records(history),
        "data_source": "yfinance / Yahoo Finance",
        "data_quality": "Live data with prototype metrics",
        "error": None,
    }

def _mock_snapshot(ticker: str, error: str | None = None) -> dict[str, Any]:
    symbol = ticker.upper().strip()
    payload = (MOCK_TICKERS.get(symbol) or DEFAULT_MOCK).copy()
    payload["ticker"] = symbol if payload["ticker"] == "MOCK" else payload["ticker"]
    payload["error"] = error
    return payload

def fetch_stock_snapshot(ticker: str, use_cache: bool = True) -> dict[str, Any]:
    symbol = ticker.upper().strip()
    if not symbol:
        return _mock_snapshot("MOCK", "No ticker provided.")
    if use_cache:
        cached = read_cached_snapshot(symbol)
        if cached:
            payload, cached_at = cached
            age_hours = (datetime.now(timezone.utc) - cached_at).total_seconds() / 3600
            if age_hours <= CACHE_MAX_AGE_HOURS:
                payload["data_quality"] = f"{payload.get('data_quality', 'Cached')} — cached {age_hours:.1f} hours ago"
                return payload
    try:
        payload = _load_yfinance_snapshot(symbol)
        cache_snapshot(symbol, payload)
        return payload
    except Exception as exc:
        fallback = _mock_snapshot(symbol, str(exc))
        cache_snapshot(symbol, fallback)
        return fallback

def fetch_many_snapshots(tickers: list[str]) -> list[dict[str, Any]]:
    return [fetch_stock_snapshot(ticker) for ticker in tickers if ticker.strip()]

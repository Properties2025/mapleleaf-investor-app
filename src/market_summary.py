"""Market summary helpers for the MapleLeaf Investor dashboard."""
from __future__ import annotations

from dataclasses import dataclass
from typing import Any

import pandas as pd

MARKET_ITEMS = [
    {"label": "S&P/TSX Composite", "ticker": "^GSPTSE", "fallback_price": 25145.20, "fallback_change": 0.62},
    {"label": "S&P 500", "ticker": "^GSPC", "fallback_price": 5297.10, "fallback_change": 0.41},
    {"label": "NASDAQ Composite", "ticker": "^IXIC", "fallback_price": 16688.29, "fallback_change": 0.64},
    {"label": "CAD / USD", "ticker": "CADUSD=X", "fallback_price": 0.7248, "fallback_change": 0.21},
    {"label": "Oil (WTI)", "ticker": "CL=F", "fallback_price": 61.62, "fallback_change": -0.88},
]


def _safe_float(value: Any) -> float | None:
    try:
        if value is None or pd.isna(value):
            return None
        return float(value)
    except Exception:
        return None


def fetch_market_summary() -> list[dict[str, Any]]:
    """Return compact market summary rows.

    Uses yfinance when internet is available, then falls back to static sample values so
    the app still renders offline.
    """
    try:
        import yfinance as yf

        tickers = [item["ticker"] for item in MARKET_ITEMS]
        data = yf.download(tickers=tickers, period="6mo", interval="1d", progress=False, group_by="ticker", auto_adjust=False, threads=True)
        rows: list[dict[str, Any]] = []
        for item in MARKET_ITEMS:
            ticker = item["ticker"]
            close = None
            try:
                if isinstance(data.columns, pd.MultiIndex):
                    close = data[ticker]["Close"].dropna()
                else:
                    close = data["Close"].dropna()
            except Exception:
                close = None

            if close is not None and len(close) >= 2:
                latest = _safe_float(close.iloc[-1])
                previous = _safe_float(close.iloc[-2])
                change = None if latest is None or previous in (None, 0) else ((latest / previous) - 1) * 100
                spark = [_safe_float(v) for v in close.tail(45).tolist() if _safe_float(v) is not None]
            else:
                latest = item["fallback_price"]
                change = item["fallback_change"]
                spark = []

            rows.append(
                {
                    "label": item["label"],
                    "ticker": ticker,
                    "price": latest,
                    "change_pct": change,
                    "sparkline": spark,
                }
            )
        return rows
    except Exception:
        return [
            {
                "label": item["label"],
                "ticker": item["ticker"],
                "price": item["fallback_price"],
                "change_pct": item["fallback_change"],
                "sparkline": [],
            }
            for item in MARKET_ITEMS
        ]

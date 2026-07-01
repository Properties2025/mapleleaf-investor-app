from __future__ import annotations
from typing import Any
from .models import RiskFlag

def clamp(value: float, low: float = 0, high: float = 100) -> int:
    return int(max(low, min(high, round(value))))

def _num(value: Any, default: float | None = None) -> float | None:
    try:
        if value is None:
            return default
        return float(value)
    except Exception:
        return default

def _growth_component(snapshot: dict[str, Any]) -> int:
    revenue_growth = _num(snapshot.get("revenue_growth"), 0) or 0
    earnings_growth = _num(snapshot.get("earnings_growth"), 0) or 0
    margins = _num(snapshot.get("profit_margins"), 0) or 0
    three_month = _num(snapshot.get("three_month_trend_pct"), 0) or 0
    one_year = _num(snapshot.get("one_year_trend_pct"), 0) or 0
    score = 45 + revenue_growth*80 + earnings_growth*50 + margins*35 + min(three_month,40)*0.35 + min(one_year,80)*0.20
    return clamp(score)

def _valuation_component(snapshot: dict[str, Any], valuation_sensitivity: str = "High") -> int:
    pe = _num(snapshot.get("forward_pe")) or _num(snapshot.get("trailing_pe"))
    ps = _num(snapshot.get("price_to_sales"))
    revenue_growth = _num(snapshot.get("revenue_growth"), 0) or 0
    score = 65
    if pe is None: score -= 5
    elif pe <= 20: score += 18
    elif pe <= 35: score += 6
    elif pe <= 55: score -= 8
    elif pe <= 80: score -= 18
    else: score -= 30
    if ps is None: score -= 3
    elif ps <= 4: score += 12
    elif ps <= 8: score += 3
    elif ps <= 15: score -= 10
    else: score -= 24
    if revenue_growth >= 0.30: score += 10
    elif revenue_growth >= 0.15: score += 5
    elif revenue_growth < 0: score -= 20
    if valuation_sensitivity == "Very High": score -= 5
    elif valuation_sensitivity == "Low": score += 5
    return clamp(score)

def _momentum_component(snapshot: dict[str, Any]) -> int:
    two_week = _num(snapshot.get("two_week_trend_pct"), 0) or 0
    three_month = _num(snapshot.get("three_month_trend_pct"), 0) or 0
    one_year = _num(snapshot.get("one_year_trend_pct"), 0) or 0
    score = 50 + min(max(two_week,-20),25)*0.9 + min(max(three_month,-40),50)*0.55 + min(max(one_year,-60),100)*0.25
    return clamp(score)

def build_risk_flags(snapshot: dict[str, Any]) -> list[RiskFlag]:
    flags = []
    revenue_growth = _num(snapshot.get("revenue_growth"))
    earnings_growth = _num(snapshot.get("earnings_growth"))
    pe = _num(snapshot.get("forward_pe")) or _num(snapshot.get("trailing_pe"))
    ps = _num(snapshot.get("price_to_sales"))
    debt_to_equity = _num(snapshot.get("debt_to_equity"))
    free_cashflow = _num(snapshot.get("free_cashflow"))
    two_week = _num(snapshot.get("two_week_trend_pct"), 0) or 0
    data_quality = str(snapshot.get("data_quality", ""))
    if "Mock" in data_quality or "Mock data" in data_quality:
        flags.append(RiskFlag("Mock or incomplete data","High","The app is using mock or incomplete data for this ticker.","Can you verify this company using a primary source before acting?"))
    if revenue_growth is not None and revenue_growth < 0:
        flags.append(RiskFlag("Falling revenue","High","Recent revenue growth appears negative.","Is the revenue decline temporary or a sign the business is weakening?"))
    if earnings_growth is not None and earnings_growth < 0:
        flags.append(RiskFlag("Falling earnings","Moderate","Recent earnings growth appears negative.","Are earnings falling because of one-time costs or a weakening business?"))
    if free_cashflow is not None and free_cashflow < 0:
        flags.append(RiskFlag("Negative free cash flow","Moderate","The company may be spending more cash than it generates.","Does the company have enough cash to fund growth without heavy dilution or debt?"))
    if debt_to_equity is not None and debt_to_equity > 120:
        flags.append(RiskFlag("High debt","High","Debt appears high relative to equity.","Can the company comfortably service debt if growth slows?"))
    if pe is not None and pe > 70:
        flags.append(RiskFlag("High valuation","Moderate","The forward or trailing P/E ratio is elevated.","Is growth strong enough to justify the price?"))
    if ps is not None and ps > 15:
        flags.append(RiskFlag("High price-to-sales","Moderate","The price-to-sales ratio is elevated.","Are margins and growth high enough to justify this sales multiple?"))
    if two_week > 25:
        flags.append(RiskFlag("Recent price spike","Moderate","The stock has risen sharply in a short period.","Is this move supported by fundamentals or just short-term excitement?"))
    return flags

def _risk_component(snapshot: dict[str, Any], flags: list[RiskFlag]) -> int:
    score = 25 + min(abs(_num(snapshot.get("two_week_trend_pct"), 0) or 0), 30) * 0.6
    for flag in flags:
        score += {"Critical":30, "High":22, "Moderate":12}.get(flag.severity, 5)
    return clamp(score)

def classify_ticker(snapshot: dict[str, Any], settings: dict[str, Any]) -> str:
    sector = str(snapshot.get("sector", "")).lower()
    ticker = str(snapshot.get("ticker", "")).upper()
    market_cap = _num(snapshot.get("market_cap"))
    if "etf" in sector or ticker in {"VFV.TO","XEQT.TO","XQQ.TO","QQQ","SPY","VTI","XIC.TO"}:
        return "ETF Alternative"
    if market_cap is not None and market_cap < 2_000_000_000:
        return "Short-Term Growth / Speculative"
    return "Long-Term Balanced Growth"

def compute_buy_score(growth: int, risk: int, valuation: int, momentum: int, category: str) -> int:
    risk_adjusted = 100 - risk
    if category == "Short-Term Growth / Speculative":
        score = 0.30*growth + 0.20*valuation + 0.35*momentum + 0.15*risk_adjusted
    elif category == "ETF Alternative":
        score = 0.20*growth + 0.25*valuation + 0.20*momentum + 0.35*risk_adjusted
    else:
        score = 0.35*growth + 0.30*valuation + 0.15*momentum + 0.20*risk_adjusted
    return clamp(score)

def score_stock(snapshot: dict[str, Any], settings: dict[str, Any]) -> dict[str, Any]:
    flags = build_risk_flags(snapshot)
    growth = _growth_component(snapshot)
    valuation = _valuation_component(snapshot, settings.get("valuation_sensitivity", "High"))
    momentum = _momentum_component(snapshot)
    risk = _risk_component(snapshot, flags)
    category = classify_ticker(snapshot, settings)
    buy_score = compute_buy_score(growth, risk, valuation, momentum, category)
    if category == "ETF Alternative":
        rating = "ETF Alternative"
    elif buy_score >= int(settings.get("buy_threshold", 80)) and risk <= int(settings.get("maximum_risk_score", 70)) and valuation >= 45:
        rating = "Buy Candidate"
    elif buy_score >= int(settings.get("watch_threshold", 60)) and risk < 85:
        rating = "Watch"
    else:
        rating = "Avoid"
    if rating == "Buy Candidate":
        reason = "The stock ranks highly on the prototype buy score, with a strong mix of growth, valuation, momentum, and risk-adjusted quality."
    elif rating == "Watch":
        reason = "The stock has some promising traits, but valuation, data quality, momentum, or risk needs more review."
    elif rating == "ETF Alternative":
        reason = "This appears to be an ETF or diversified fund that may be useful as a benchmark or lower-maintenance alternative."
    else:
        reason = "The stock does not currently meet the prototype buy-ranking threshold."
    main_risk = flags[0].explanation if flags else "No major prototype risk flag was detected, but this is not a full due-diligence review."
    next_step = "Compare fees, holdings, diversification, and overlap with your existing portfolio." if rating == "ETF Alternative" else "Review recent earnings, valuation versus peers, and whether the growth thesis is still reasonable."
    return {
        "buy_score": buy_score, "growth_score": growth, "risk_score": risk,
        "valuation_score": valuation, "momentum_score": momentum, "rating": rating,
        "category": category, "reason": reason, "main_risk": main_risk,
        "next_step": next_step, "risk_flags": flags,
    }

def score_to_label(score: int, reverse: bool = False) -> str:
    if reverse:
        if score <= 30: return "Low"
        if score <= 60: return "Moderate"
        return "High"
    if score >= 80: return "Strong"
    if score >= 60: return "Moderate"
    return "Weak"

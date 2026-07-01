from __future__ import annotations
from dataclasses import dataclass, field
from typing import Any

@dataclass
class RiskFlag:
    name: str
    severity: str
    explanation: str
    research_question: str

@dataclass
class StockSnapshot:
    ticker: str
    company_name: str
    market: str
    sector: str
    industry: str
    current_price: float | None
    currency: str
    daily_change_pct: float | None
    two_week_trend_pct: float | None
    three_month_trend_pct: float | None
    one_year_trend_pct: float | None
    market_cap: float | None
    trailing_pe: float | None
    forward_pe: float | None
    price_to_sales: float | None
    revenue_growth: float | None
    earnings_growth: float | None
    profit_margins: float | None
    debt_to_equity: float | None
    free_cashflow: float | None
    total_cash: float | None
    history: list[dict[str, Any]]
    data_source: str
    data_quality: str
    error: str | None = None

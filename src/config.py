from __future__ import annotations

DEFAULT_SETTINGS = {
    "market_universe": "Canada + U.S.",
    "short_term_risk_tolerance": "Aggressive / Speculative",
    "long_term_risk_tolerance": "Balanced Growth",
    "valuation_sensitivity": "High",
    "minimum_market_cap": 300_000_000,
    "maximum_risk_score": 70,
    "include_etfs": True,
    "show_beginner_explanations": True,
    "show_advanced_metrics": False,
    "prioritize": "Balanced",
    "short_term_horizon": "2 weeks to 6 months",
    "long_term_horizon": "5 to 10 years",
    "buy_threshold": 80,
    "watch_threshold": 60,
    "trim_threshold": 65,
    "sell_threshold": 80,
    "preferred_sectors": [],
    "excluded_sectors": [],
    "alert_preferences": [
        "New Buy Candidate", "Valuation Warning", "Momentum Breakdown",
        "Risk Score Spike", "Sell Candidate", "Trim Candidate"
    ],
    "email_daily_digest_enabled": False,
    "email_recipient": "",
    "email_top_n": 5,
    "email_include_watchlist": True,
    "email_include_etfs": True,
}

WATCHLIST_DEFAULT = ["SHOP.TO", "RY.TO", "MSFT", "NVDA", "AAPL", "VFV.TO"]
ETF_HINTS = {"VFV.TO", "XEQT.TO", "XQQ.TO", "QQQ", "SPY", "VTI", "XIC.TO"}

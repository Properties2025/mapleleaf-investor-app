from src.scoring import score_stock, compute_buy_score

def test_score_stock_returns_expected_keys():
    snapshot = {
        "ticker":"TEST", "company_name":"Test Co", "market":"U.S.", "sector":"Technology",
        "current_price":100.0, "daily_change_pct":1.0, "two_week_trend_pct":3.0,
        "three_month_trend_pct":10.0, "one_year_trend_pct":25.0, "market_cap":10_000_000_000,
        "trailing_pe":30.0, "forward_pe":25.0, "price_to_sales":6.0, "revenue_growth":0.20,
        "earnings_growth":0.15, "profit_margins":0.18, "debt_to_equity":20.0,
        "free_cashflow":100_000_000, "data_quality":"Test",
    }
    settings = {"valuation_sensitivity":"High", "buy_threshold":80, "watch_threshold":60, "maximum_risk_score":70}
    score = score_stock(snapshot, settings)
    assert "buy_score" in score
    assert "growth_score" in score
    assert score["rating"] in {"Buy Candidate", "Watch", "Avoid", "ETF Alternative"}

def test_compute_buy_score_bounds():
    score = compute_buy_score(100, 0, 100, 100, "Long-Term Balanced Growth")
    assert 0 <= score <= 100

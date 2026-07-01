from __future__ import annotations
from datetime import date

CONCEPTS = [
    {"term":"Revenue growth","explanation":"Revenue growth shows whether a company is selling more over time. For growth investors, steady revenue growth can be a sign the business is expanding."},
    {"term":"Free cash flow","explanation":"Free cash flow is cash left after a company pays for operations and investments. Positive free cash flow gives a company more flexibility."},
    {"term":"Valuation risk","explanation":"Valuation risk means a good company may still be a poor investment if the stock price already assumes too much future growth."},
    {"term":"P/E ratio","explanation":"The price-to-earnings ratio compares a company’s stock price to its earnings. A high P/E can be reasonable for a fast grower, but it raises expectations."},
    {"term":"Price-to-sales ratio","explanation":"The price-to-sales ratio compares the company’s value to its revenue. It is often used for growth companies, especially when earnings are still developing."},
    {"term":"Momentum","explanation":"Momentum measures whether a stock’s price has been moving up or down. It can help identify interest in a stock, but it can reverse quickly."},
    {"term":"Risk score","explanation":"A risk score combines warning signs like high debt, weak cash flow, declining growth, high valuation, volatility, or incomplete data."},
    {"term":"Watchlist","explanation":"A watchlist is a group of stocks you are interested in but may not be ready to buy. It helps you track whether the business or price improves."},
]

def concept_of_the_day() -> dict[str, str]:
    return CONCEPTS[date.today().toordinal() % len(CONCEPTS)]

def explain_metric(metric: str) -> str:
    normalized = metric.lower().strip()
    for concept in CONCEPTS:
        if normalized in concept["term"].lower():
            return concept["explanation"]
    return "This metric is part of the app’s research model. Use it as a starting point for further research, not as a standalone decision."

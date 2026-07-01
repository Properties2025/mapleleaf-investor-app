"""Reusable Streamlit UI components for the MapleLeaf Investor interface."""
from __future__ import annotations

import html
from typing import Any

import pandas as pd
import streamlit as st

INDICATOR_HELP = {
    "Buy Ranking": "Overall 0–100 ranking that blends growth, valuation, momentum, and risk. Higher means the stock ranks better within your current watchlist.",
    "Growth": "How strongly the company appears to be growing based on prototype revenue, earnings, margins, and trend data.",
    "Risk": "Warning score for volatility, weak fundamentals, high valuation, high debt, or incomplete data. Lower is better.",
    "Valuation": "How reasonable the stock price appears relative to earnings, sales, and growth. Higher is better.",
    "Dividend Yield": "Annual dividends divided by the current stock price. Useful for income stocks, but not required for growth stocks.",
    "Payout Ratio": "The share of earnings paid as dividends. Lower values may leave more room for reinvestment and growth.",
    "P/E Ratio": "Price-to-earnings ratio. It compares the stock price to earnings. Higher values may signal high expectations or valuation risk.",
    "Price/Sales": "Price-to-sales ratio. It compares company value to revenue. Useful for growth stocks, but can become stretched.",
    "Free Cash Flow": "Cash left after operating and capital spending. Positive free cash flow gives a company more flexibility.",
    "Debt/Equity": "A leverage ratio. Higher values can mean more financial risk, especially if growth slows.",
}


def apply_mapleleaf_theme() -> None:
    """CSS theme that follows the supplied MapleLeaf Investor concept."""
    st.markdown(
        """
        <style>
        :root {
            --navy: #082046;
            --navy-2: #0e2d5d;
            --ink: #101828;
            --muted: #667085;
            --line: #dbe4f0;
            --soft-line: #edf2f7;
            --panel: #ffffff;
            --bg: #f5f8fc;
            --blue: #174a8b;
            --blue-2: #2563eb;
            --green: #16a34a;
            --red: #dc2626;
            --amber: #d97706;
        }
        .stApp { background: var(--bg); }
        .main .block-container { padding-top: .35rem; max-width: 1680px; padding-left: 1rem; padding-right: 1rem; }
        [data-testid="stSidebar"] { background: linear-gradient(180deg, #061a39 0%, #082046 55%, #0e2d5d 100%); width: 5.8rem !important; min-width: 5.8rem !important; }
        [data-testid="stSidebar"] * { color: white !important; }
        [data-testid="stSidebar"] .stRadio > label { display:none; }
        [data-testid="stSidebar"] [role="radiogroup"] label { border-radius: 12px; padding: 0.42rem 0.35rem; margin-bottom: .25rem; }
        [data-testid="stSidebar"] [role="radiogroup"] label:hover { background: rgba(255,255,255,.10); }
        [data-testid="stSidebar"] [aria-checked="true"] { background: rgba(255,255,255,.15); box-shadow: inset 3px 0 0 #ffffff; }
        .maple-brand { text-align:center; padding: 10px 0 14px 0; }
        .maple-leaf { font-size: 2.35rem; line-height: 1; }
        .maple-proud { margin-top: 1.2rem; border: 1px solid rgba(255,255,255,.18); border-radius: 14px; padding: 8px 4px; font-size: .75rem; text-align:center; }
        .top-brand-row { display:flex; align-items:center; gap:14px; margin: 3px 0 8px 0; }
        .top-brand-leaf { font-size:2.8rem; line-height:1; }
        .top-brand-title { font-size:2.15rem; line-height: .95; font-weight: 800; color: #0f1f3a; }
        .top-brand-title span { color:#ef4444; font-weight:780; }
        .market-summary { background: #fff; border: 1px solid var(--line); border-radius: 12px; padding: 12px 14px; box-shadow: 0 5px 18px rgba(15,23,42,.04); }
        .market-summary-header { display:flex; justify-content:space-between; align-items:center; border-bottom:1px solid var(--soft-line); padding-bottom:8px; margin-bottom:8px; font-weight:780; color:var(--ink); }
        .market-grid { display:grid; grid-template-columns: repeat(5, minmax(125px,1fr)) minmax(260px,1.4fr) auto; gap: 10px; align-items:center; }
        .market-item { border-right:1px solid var(--line); padding-right:10px; min-height:60px; }
        .market-label { color:#344054; font-size:.84rem; font-weight:700; }
        .market-price { color:#101828; font-size:1.05rem; font-weight:800; margin-top:3px; }
        .market-change-pos { color: var(--green); font-weight:800; font-size:.82rem; }
        .market-change-neg { color: var(--red); font-weight:800; font-size:.82rem; }
        .takeaway { color:#344054; font-size:.82rem; line-height:1.35; }
        .email-btn { background:#0e2d5d; color:white; padding:11px 14px; border-radius:9px; text-align:center; font-weight:800; white-space:nowrap; }
        .panel { background: #fff; border: 1px solid var(--line); border-radius: 12px; box-shadow: 0 6px 18px rgba(15,23,42,.045); }
        .panel-pad { padding: 14px; }
        .panel-title { font-size:1.12rem; font-weight:800; color:#101828; display:flex; align-items:center; gap:6px; margin-bottom:10px; }
        .toolbar { display:flex; justify-content:space-between; align-items:center; gap:10px; margin-bottom:9px; }
        .chip { display:inline-flex; align-items:center; gap:6px; border:1px solid #bdd1ee; color:#174a8b; background:#f4f8ff; border-radius:8px; padding:7px 10px; font-size:.82rem; font-weight:700; }
        .quote-header { background:#fff; border:1px solid var(--line); border-radius:12px; padding:13px 14px; margin-bottom:10px; }
        .quote-top { display:flex; align-items:center; justify-content:space-between; gap:12px; }
        .company-block { display:flex; align-items:center; gap:13px; }
        .logo-box { width:54px; height:54px; border-radius:10px; background:linear-gradient(135deg,#1e3a8a,#2563eb); color:#fff; display:flex; align-items:center; justify-content:center; font-weight:900; font-size:1.2rem; border: 3px solid #dbeafe; }
        .ticker-line { display:flex; align-items:baseline; gap:8px; color:#101828; font-weight:800; }
        .ticker-symbol { font-size:1.25rem; }
        .company-name { font-size:.95rem; color:#344054; font-weight:700; }
        .price-line { font-size:1.72rem; font-weight:850; color:#101828; margin-top:4px; }
        .positive { color:var(--green); font-weight:800; }
        .negative { color:var(--red); font-weight:800; }
        .tabs-line { border-top:1px solid var(--soft-line); margin-top:12px; padding-top:10px; display:flex; gap:24px; color:#344054; font-weight:700; font-size:.88rem; }
        .tabs-line span:first-child { color:#174a8b; border-bottom:3px solid #174a8b; padding-bottom:8px; }
        .summary-card { background:#fff; border:1px solid var(--line); border-radius:12px; padding:14px; height:100%; }
        .summary-title { font-size:1rem; font-weight:820; color:#101828; margin-bottom:10px; display:flex; gap:6px; align-items:center; }
        .thesis { color:#344054; line-height:1.45; font-size:.92rem; }
        .stat-row { display:flex; justify-content:space-between; border-bottom:1px solid var(--soft-line); padding:8px 0; font-size:.9rem; }
        .stat-row div:first-child { color:#475467; }
        .stat-row div:last-child { color:#101828; font-weight:750; }
        .value-big { font-size:1.55rem; font-weight:850; color:#101828; }
        .upside { font-size:1.25rem; font-weight:850; color:var(--green); }
        .indicator-grid { display:grid; grid-template-columns: repeat(3, minmax(220px,1fr)); gap:14px; }
        .indicator-tile { display:flex; gap:11px; align-items:flex-start; padding:12px; border-radius:12px; background:#fff; border:1px solid var(--soft-line); }
        .indicator-icon { width:38px; height:38px; border-radius:50%; display:flex; align-items:center; justify-content:center; color:#fff; font-weight:900; flex-shrink:0; }
        .indicator-name { font-weight:800; color:#101828; }
        .indicator-copy { color:#475467; font-size:.82rem; line-height:1.35; }
        .reminder-box { border:1px solid var(--line); border-radius:12px; background:#fff; padding:14px; color:#344054; display:flex; justify-content:space-between; gap:20px; align-items:center; }
        div[data-testid="stMetric"] { background:#fff; border:1px solid var(--line); border-radius:12px; padding: 10px 12px; }
        .stDataFrame { border-radius: 12px; overflow:hidden; }
        button[kind="primary"] { background:#0e2d5d !important; border-color:#0e2d5d !important; }
        </style>
        """,
        unsafe_allow_html=True,
    )


def render_sidebar_brand() -> None:
    st.sidebar.markdown(
        """
        <div class="maple-brand">
            <div class="maple-leaf">🍁</div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def render_page_brand() -> None:
    st.markdown(
        """
        <div class="top-brand-row">
            <div class="top-brand-leaf">🍁</div>
            <div class="top-brand-title">MapleLeaf<br><span>Investor</span></div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def format_money(value: float | None, currency: str = "") -> str:
    if value is None:
        return "N/A"
    try:
        return f"{currency} ${value:,.2f}".strip()
    except Exception:
        return "N/A"


def format_large_number(value: float | None) -> str:
    if value is None:
        return "N/A"
    try:
        value = float(value)
        if abs(value) >= 1_000_000_000_000:
            return f"{value / 1_000_000_000_000:.2f}T"
        if abs(value) >= 1_000_000_000:
            return f"{value / 1_000_000_000:.2f}B"
        if abs(value) >= 1_000_000:
            return f"{value / 1_000_000:.2f}M"
        return f"{value:,.0f}"
    except Exception:
        return "N/A"


def format_pct(value: float | None, already_pct: bool = True) -> str:
    if value is None:
        return "N/A"
    try:
        return f"{value:.2f}%" if already_pct else f"{value * 100:.2f}%"
    except Exception:
        return "N/A"


def format_ratio(value: float | None) -> str:
    if value is None:
        return "N/A"
    try:
        return f"{value:.2f}"
    except Exception:
        return "N/A"


def score_label(score: int, reverse: bool = False) -> str:
    if reverse:
        if score <= 30:
            return "Low"
        if score <= 60:
            return "Moderate"
        return "High"
    if score >= 80:
        return "Excellent"
    if score >= 65:
        return "Good"
    if score >= 50:
        return "Fair"
    return "Caution"


def render_disclaimer(compact: bool = True) -> None:
    text = "Research tool only. Ratings are prototype research signals, not financial advice, trade instructions, or guaranteed outcomes."
    if compact:
        st.caption(text)
    else:
        st.info(text)


def render_daily_market_summary(summary: list[dict[str, Any]]) -> None:
    item_html = []
    for item in summary:
        change = item.get("change_pct")
        change_class = "market-change-pos" if change is None or change >= 0 else "market-change-neg"
        arrow = "+" if change is not None and change >= 0 else ""
        price = item.get("price")
        price_text = f"{price:,.4f}" if item.get("label") == "CAD / USD" and price is not None else (f"{price:,.2f}" if price is not None else "N/A")
        item_html.append(
            f"""
            <div class="market-item">
                <div class="market-label">{html.escape(str(item.get('label', 'Market')))}</div>
                <div class="market-price">{price_text}</div>
                <div class="{change_class}">{arrow}{format_pct(change)}</div>
            </div>
            """
        )
    st.markdown(
        f"""
        <div class="market-summary">
            <div class="market-summary-header">
                <div>Daily Market Summary <span style="color:#f59e0b;">☀</span> <span style="font-weight:500;color:#667085;">Today • Market data preview</span></div>
            </div>
            <div class="market-grid">
                {''.join(item_html)}
                <div class="takeaway"><b>Market Takeaway</b><br>Use this row as your high-level context before reviewing individual stock ideas. Watch whether broad markets support or conflict with your stock-specific signals.</div>
                <div class="email-btn">✉ Email Overview</div>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def build_ranked_watchlist_rows(scored_items: list[tuple[dict, dict]]) -> pd.DataFrame:
    rows = []
    for snapshot, score in scored_items:
        rows.append(
            {
                "Stock": snapshot.get("ticker"),
                "Company": snapshot.get("company_name"),
                "Price": snapshot.get("current_price"),
                "Daily %": snapshot.get("daily_change_pct"),
                "Buy Ranking": score.get("buy_score"),
                "Growth": score.get("growth_score"),
                "Risk": score.get("risk_score"),
                "Valuation": score.get("valuation_score"),
                "Momentum": score.get("momentum_score"),
                "Rating": score.get("rating"),
                "Sector": snapshot.get("sector"),
                "Category": score.get("category"),
                "Notes": score.get("main_risk"),
            }
        )
    df = pd.DataFrame(rows)
    if df.empty:
        return df
    df = df.sort_values("Buy Ranking", ascending=False).reset_index(drop=True)
    df.insert(0, "Rank", range(1, len(df) + 1))
    return df


def render_score_help(label: str) -> None:
    text = INDICATOR_HELP.get(label, "A prototype indicator used by the app to support research.")
    if hasattr(st, "popover"):
        with st.popover(f"{label} ⓘ"):
            st.write(text)
    else:
        with st.expander(f"{label} ⓘ"):
            st.write(text)


def render_watchlist_table(df: pd.DataFrame, height: int = 640) -> None:
    if df.empty:
        st.warning("Your watchlist is empty. Add tickers to begin.")
        return
    st.dataframe(
        df,
        use_container_width=True,
        hide_index=True,
        height=height,
        column_config={
            "Rank": st.column_config.NumberColumn("", width="small", help="Default rank when sorted by Buy Ranking."),
            "Stock": st.column_config.TextColumn("Stock", width="medium"),
            "Company": st.column_config.TextColumn("Company", width="medium"),
            "Buy Ranking": st.column_config.ProgressColumn("Buy Ranking", help=INDICATOR_HELP["Buy Ranking"], min_value=0, max_value=100, format="%d"),
            "Growth": st.column_config.ProgressColumn("Growth", help=INDICATOR_HELP["Growth"], min_value=0, max_value=100, format="%d"),
            "Risk": st.column_config.ProgressColumn("Risk", help=INDICATOR_HELP["Risk"], min_value=0, max_value=100, format="%d"),
            "Valuation": st.column_config.ProgressColumn("Valuation", help=INDICATOR_HELP["Valuation"], min_value=0, max_value=100, format="%d"),
            "Momentum": st.column_config.ProgressColumn("Momentum", help=INDICATOR_HELP["Buy Ranking"], min_value=0, max_value=100, format="%d"),
            "Price": st.column_config.NumberColumn("Price", format="$%.2f", width="small"),
            "Daily %": st.column_config.NumberColumn("Daily %", format="%.2f%%", width="small"),
            "Notes": st.column_config.TextColumn("Notes", width="large"),
        },
    )


def render_smart_watchlist(scored: list[tuple[dict, dict]], watchlist: list[str]) -> str | None:
    ranked_df = build_ranked_watchlist_rows(scored)
    st.markdown('<div class="panel"><div class="panel-pad">', unsafe_allow_html=True)
    top_left, top_right = st.columns([1.1, 1])
    with top_left:
        st.markdown('<div class="panel-title">Smart Watchlist ⓘ</div>', unsafe_allow_html=True)
    with top_right:
        selected_list = st.selectbox("Watchlist", ["My Core Watchlist"], label_visibility="collapsed")
    controls = st.columns([1, .7, .7])
    with controls[0]:
        st.markdown('<span class="chip">Sorted by: Buy Ranking ✕</span>', unsafe_allow_html=True)
    with controls[1]:
        st.button("＋ Add Filter")
    with controls[2]:
        st.caption("Last updated: now ↻")
    render_watchlist_table(ranked_df)
    render_disclaimer()
    st.markdown('</div></div>', unsafe_allow_html=True)
    if ranked_df.empty:
        return None
    return st.selectbox("Select stock for detail panel", ranked_df["Stock"].tolist(), label_visibility="collapsed")


def _change_class(value: float | None) -> str:
    if value is None or value >= 0:
        return "positive"
    return "negative"


def _change_text(value: float | None) -> str:
    if value is None:
        return "N/A"
    sign = "+" if value >= 0 else ""
    return f"{sign}{value:.2f}%"


def render_quote_header(snapshot: dict, score: dict) -> None:
    ticker = snapshot.get("ticker", "N/A")
    name = snapshot.get("company_name", ticker)
    price = snapshot.get("current_price")
    currency = snapshot.get("currency", "")
    change = snapshot.get("daily_change_pct")
    logo = ticker[:2].replace(".", "")
    st.markdown(
        f"""
        <div class="quote-header">
            <div class="quote-top">
                <div class="company-block">
                    <div class="logo-box">{html.escape(logo)}</div>
                    <div>
                        <div class="ticker-line"><span class="ticker-symbol">{html.escape(ticker)}</span><span class="company-name">{html.escape(name)}</span></div>
                        <div style="color:#667085;font-size:.85rem;">{html.escape(str(snapshot.get('sector','Unknown')))} • {html.escape(str(score.get('category','Unknown')))}</div>
                        <div class="price-line">{format_money(price, currency)} <span class="{_change_class(change)}" style="font-size:.95rem;">{_change_text(change)}</span></div>
                    </div>
                </div>
                <div style="display:flex; gap:8px; align-items:center;"><span class="chip">☆ Add to Portfolio</span><span class="chip">⋮</span></div>
            </div>
            <div class="tabs-line"><span>Overview</span><span>Financials</span><span>Forecasts</span><span>News</span><span>Valuation</span><span>Peers</span><span>Notes</span></div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def render_chart_panel(snapshot: dict) -> None:
    st.markdown('<div class="summary-card"><div class="summary-title">Price Chart ⓘ</div>', unsafe_allow_html=True)
    ranges = st.columns(8)
    for col, label in zip(ranges, ["1D", "5D", "1M", "3M", "6M", "YTD", "1Y", "5Y"]):
        col.caption(f"**{label}**" if label == "1Y" else label)
    history = snapshot.get("history") or []
    if history:
        df = pd.DataFrame(history)
        if not df.empty and {"date", "close"}.issubset(df.columns):
            df["date"] = pd.to_datetime(df["date"], errors="coerce")
            df = df.dropna(subset=["date", "close"]).set_index("date")
            st.line_chart(df["close"], height=250)
        else:
            st.info("No chart data available.")
    else:
        st.info("No chart data available.")
    st.markdown('</div>', unsafe_allow_html=True)


def render_analyst_summary(snapshot: dict, score: dict) -> None:
    growth = score.get("growth_score", 0)
    risk = score.get("risk_score", 0)
    valuation = score.get("valuation_score", 0)
    moat = "Strong" if growth >= 75 else "Moderate" if growth >= 60 else "Developing"
    balance = "Very Strong" if risk <= 30 else "Review" if risk <= 60 else "Elevated Risk"
    business_quality = "Excellent" if growth >= 80 else "Good" if growth >= 65 else "Fair"
    rows = [
        ("Business Quality", business_quality, f"{max(5, min(9, round(growth/11)))}/10"),
        ("Competitive Advantage", moat, f"{max(4, min(8, round(growth/12)))}/10"),
        ("Management", "Unknown", "—"),
        ("Balance Sheet", balance, f"{max(3, min(9, round((100-risk)/11)))}/10"),
        ("Moat Trend", "Stable", "—"),
    ]
    st.markdown('<div class="summary-card"><div class="summary-title">Analyst Style Summary ⓘ</div>', unsafe_allow_html=True)
    for label, value, mark in rows:
        val_class = "positive" if value in {"Excellent", "Strong", "Good", "Very Strong", "Stable"} else "negative" if value == "Elevated Risk" else ""
        st.markdown(f'<div class="stat-row"><div>{html.escape(label)}</div><div><span class="{val_class}">{html.escape(value)}</span> &nbsp; {html.escape(mark)}</div></div>', unsafe_allow_html=True)
    st.markdown('<div style="height:12px"></div><div class="summary-title">Overall Thesis ⓘ</div>', unsafe_allow_html=True)
    st.markdown(f'<div class="thesis">{html.escape(score.get("reason", "Review the company before acting."))}</div>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)


def render_value_card(snapshot: dict, score: dict) -> None:
    price = snapshot.get("current_price") or 0
    valuation = score.get("valuation_score", 50)
    # Prototype fair value estimate: more generous when valuation score is high, stricter when low.
    fair = price * (0.80 + valuation / 100 * 0.45) if price else None
    upside = None if fair is None or not price else ((fair / price) - 1) * 100
    st.markdown('<div class="summary-card"><div class="summary-title">Intrinsic Value Estimate ⓘ</div>', unsafe_allow_html=True)
    st.markdown(f'<div class="value-big">{format_money(fair, snapshot.get("currency", ""))}</div>', unsafe_allow_html=True)
    st.markdown(f'<div class="upside">{_change_text(upside)} upside</div>', unsafe_allow_html=True)
    st.progress(max(0, min(100, valuation)))
    st.caption("Prototype estimate only. Future versions should use a more robust valuation model.")
    st.markdown('</div>', unsafe_allow_html=True)


def render_dividend_card(snapshot: dict) -> None:
    # yfinance prototype does not always include dividend details in our snapshot, so show friendly placeholders.
    st.markdown('<div class="summary-card"><div class="summary-title">Dividend Highlights ⓘ</div>', unsafe_allow_html=True)
    for label, value in [("Dividend Yield", "Data pending"), ("Payout Ratio", "Data pending"), ("Dividend Growth", "Data pending"), ("Years of Increases", "Data pending")]:
        st.markdown(f'<div class="stat-row"><div>{label}</div><div>{value}</div></div>', unsafe_allow_html=True)
    st.caption("Dividend metrics will be expanded in the holdings and income modules.")
    st.markdown('</div>', unsafe_allow_html=True)


def render_earnings_card(snapshot: dict) -> None:
    st.markdown('<div class="summary-card"><div class="summary-title">Earnings Highlights ⓘ</div>', unsafe_allow_html=True)
    rows = [
        ("Revenue Growth", format_pct(snapshot.get("revenue_growth"), already_pct=False)),
        ("Earnings Growth", format_pct(snapshot.get("earnings_growth"), already_pct=False)),
        ("Profit Margin", format_pct(snapshot.get("profit_margins"), already_pct=False)),
        ("Forward P/E", format_ratio(snapshot.get("forward_pe"))),
    ]
    for label, value in rows:
        st.markdown(f'<div class="stat-row"><div>{label}</div><div>{value}</div></div>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)


def render_stock_detail(snapshot: dict, score: dict) -> None:
    render_quote_header(snapshot, score)
    top_left, top_right = st.columns([1.08, .92], gap="medium")
    with top_left:
        render_chart_panel(snapshot)
    with top_right:
        render_analyst_summary(snapshot, score)
    bottom = st.columns(3, gap="medium")
    with bottom[0]:
        render_value_card(snapshot, score)
    with bottom[1]:
        render_dividend_card(snapshot)
    with bottom[2]:
        render_earnings_card(snapshot)


def render_indicator_tiles() -> None:
    st.markdown('<div class="panel"><div class="panel-pad"><div class="panel-title">Understand the Indicators ⓘ</div>', unsafe_allow_html=True)
    tiles = [
        ("★", "Buy Ranking", INDICATOR_HELP["Buy Ranking"], "#16a34a"),
        ("🛡", "Risk", INDICATOR_HELP["Risk"], "#46b97c"),
        ("$", "Dividend Yield", INDICATOR_HELP["Dividend Yield"], "#0f6fb7"),
        ("↗", "Growth", INDICATOR_HELP["Growth"], "#65a30d"),
        ("◆", "Valuation", INDICATOR_HELP["Valuation"], "#0ea5e9"),
        ("%", "Payout Ratio", INDICATOR_HELP["Payout Ratio"], "#9333ea"),
    ]
    html_tiles = []
    for icon, name, copy, colour in tiles:
        html_tiles.append(
            f"""
            <div class="indicator-tile">
                <div class="indicator-icon" style="background:{colour};">{icon}</div>
                <div><div class="indicator-name">{html.escape(name)}</div><div class="indicator-copy">{html.escape(copy)}</div></div>
            </div>
            """
        )
    st.markdown(f'<div class="indicator-grid">{"".join(html_tiles)}</div></div></div>', unsafe_allow_html=True)


def render_reminder_box() -> None:
    st.markdown(
        """
        <div class="reminder-box">
            <div><b>Remember</b><br>These tools are here to help you learn and do your research. Always consider your goals, time horizon, and risk tolerance.</div>
            <div><b>New to investing?</b><br><span style="color:#174a8b;font-weight:800;">Visit the Education Center →</span></div>
        </div>
        """,
        unsafe_allow_html=True,
    )

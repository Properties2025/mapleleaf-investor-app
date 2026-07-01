from __future__ import annotations

from datetime import date

import pandas as pd
import streamlit as st

from src.config import DEFAULT_SETTINGS
from src.data_provider import fetch_many_snapshots
from src.email_digest import build_digest_text, send_digest_email
from src.explainers import concept_of_the_day, explain_metric
from src.market_summary import fetch_market_summary
from src.scoring import score_stock
from src.storage import load_settings, load_watchlist, save_settings, save_watchlist
from src.ui_components import (
    apply_mapleleaf_theme,
    build_ranked_watchlist_rows,
    render_daily_market_summary,
    render_disclaimer,
    render_indicator_tiles,
    render_page_brand,
    render_reminder_box,
    render_score_help,
    render_sidebar_brand,
    render_smart_watchlist,
    render_stock_detail,
    render_watchlist_table,
)

st.set_page_config(page_title="MapleLeaf Investor", page_icon="🍁", layout="wide")
apply_mapleleaf_theme()

settings = load_settings()
watchlist = load_watchlist()

render_sidebar_brand()
page = st.sidebar.radio(
    "Navigation",
    ["⌂\nHome", "☆\nWatchlist", "⌕\nResearch", "☷\nScreener", "◔\nPortfolios", "▰\nEducation", "☰\nNews", "⚙\nSettings", "?\nHelp"],
    label_visibility="collapsed",
)
st.sidebar.markdown('<div class="maple-proud">🍁<br>Proudly<br>Canadian</div>', unsafe_allow_html=True)


def get_scored_watchlist() -> list[tuple[dict, dict]]:
    snapshots = fetch_many_snapshots(watchlist)
    return [(snapshot, score_stock(snapshot, settings)) for snapshot in snapshots]


def find_selected_pair(scored: list[tuple[dict, dict]], selected: str | None) -> tuple[dict, dict] | None:
    if not scored:
        return None
    if not selected:
        return scored[0]
    return next(((snapshot, score) for snapshot, score in scored if snapshot.get("ticker") == selected), scored[0])


def render_header() -> None:
    brand_col, summary_col = st.columns([0.16, 0.84], gap="medium")
    with brand_col:
        render_page_brand()
    with summary_col:
        render_daily_market_summary(fetch_market_summary())


render_header()

if page.startswith("⌂") or page.startswith("☆"):
    with st.spinner("Loading watchlist and market data..."):
        scored = get_scored_watchlist()
    ranked_df = build_ranked_watchlist_rows(scored)

    left, right = st.columns([0.42, 0.58], gap="medium")
    with left:
        selected_ticker = render_smart_watchlist(scored, watchlist)
        with st.expander("Edit watchlist tickers"):
            st.write("Use `.TO` for many TSX-listed Canadian tickers, such as `SHOP.TO`, `RY.TO`, or `VFV.TO`.")
            new_watchlist_text = st.text_area("Watchlist tickers", value=", ".join(watchlist), height=110)
            if st.button("Save Watchlist", type="primary"):
                save_watchlist([t.strip().upper() for t in new_watchlist_text.split(",") if t.strip()])
                st.success("Watchlist saved. Refreshing...")
                st.rerun()

    selected_pair = find_selected_pair(scored, selected_ticker)
    with right:
        if selected_pair:
            snapshot, score = selected_pair
            render_stock_detail(snapshot, score)
        else:
            st.warning("Add watchlist tickers to populate the stock detail panel.")

    st.write("")
    render_indicator_tiles()
    st.write("")
    render_reminder_box()

elif page.startswith("⌕"):
    st.markdown("## Research")
    st.info("This page will become the deeper research workspace. For now, select stocks from the Watchlist/Home page to view the full detail panel.")
    with st.spinner("Loading watchlist data..."):
        scored = get_scored_watchlist()
    ranked_df = build_ranked_watchlist_rows(scored)
    if not ranked_df.empty:
        selected = st.selectbox("Choose a stock to research", ranked_df["Stock"].tolist())
        pair = find_selected_pair(scored, selected)
        if pair:
            render_stock_detail(*pair)

elif page.startswith("☷"):
    st.markdown("## Screener")
    st.info("Placeholder for the future Canadian/U.S. stock discovery screener. It will separate short-term speculative ideas from long-term balanced growth ideas.")
    st.markdown(
        """
        Planned filters:
        - Market: Canada, U.S., or both
        - Market cap range
        - Minimum Buy Ranking
        - Maximum Risk
        - Growth threshold
        - Valuation threshold
        - Sector include/exclude
        - ETF alternatives
        """
    )

elif page.startswith("◔"):
    st.markdown("## Portfolios")
    st.info("Placeholder for the holdings tracker and future Hold / Review / Trim / Sell Candidate engine.")
    st.markdown(
        """
        Planned holding fields:
        - Ticker
        - Company name
        - Number of shares
        - Average cost
        - Account type
        - Holding category: Short-Term, Long-Term, ETF, or Unknown
        - Purchase date
        - Original thesis
        """
    )

elif page.startswith("▰"):
    st.markdown("## Education Center")
    concept = concept_of_the_day()
    st.subheader("Daily investing concept")
    st.info(f"**{concept['term']}** — {concept['explanation']}")
    st.subheader("Understand an indicator")
    terms = list(
        {
            "Buy Ranking": None,
            "Growth": None,
            "Risk": None,
            "Valuation": None,
            "P/E Ratio": None,
            "Price/Sales": None,
            "Free Cash Flow": None,
            "Debt/Equity": None,
        }.keys()
    )
    selected = st.selectbox("Choose a topic", terms)
    render_score_help(selected)
    st.write(explain_metric(selected))
    render_indicator_tiles()

elif page.startswith("☰"):
    st.markdown("## News")
    st.info("Placeholder for future market news, major company events, analyst updates, and risk alerts.")

elif page.startswith("⚙"):
    st.markdown("## Settings")

    with st.form("settings_form"):
        market_universe = st.selectbox(
            "Market universe",
            ["Canada + U.S.", "Canada only", "U.S. only"],
            index=["Canada + U.S.", "Canada only", "U.S. only"].index(settings.get("market_universe", "Canada + U.S.")),
        )
        short_term_risk = st.selectbox(
            "Short-term risk tolerance",
            ["Aggressive / Speculative", "Balanced", "Conservative"],
            index=["Aggressive / Speculative", "Balanced", "Conservative"].index(settings.get("short_term_risk_tolerance", "Aggressive / Speculative")),
        )
        long_term_risk = st.selectbox(
            "Long-term risk tolerance",
            ["Balanced Growth", "Aggressive Growth", "Conservative Growth"],
            index=["Balanced Growth", "Aggressive Growth", "Conservative Growth"].index(settings.get("long_term_risk_tolerance", "Balanced Growth")),
        )
        valuation_sensitivity = st.selectbox(
            "Valuation sensitivity",
            ["Very High", "High", "Moderate", "Low"],
            index=["Very High", "High", "Moderate", "Low"].index(settings.get("valuation_sensitivity", "High")),
        )
        a, b = st.columns(2)
        with a:
            minimum_market_cap = st.number_input("Minimum market cap", min_value=0, value=int(settings.get("minimum_market_cap", 300_000_000)), step=50_000_000)
            maximum_risk_score = st.slider("Maximum risk score for Buy Candidate", 0, 100, int(settings.get("maximum_risk_score", 70)))
        with b:
            buy_threshold = st.slider("Buy Candidate threshold", 0, 100, int(settings.get("buy_threshold", 80)))
            watch_threshold = st.slider("Watch threshold", 0, 100, int(settings.get("watch_threshold", 60)))
        include_etfs = st.checkbox("Include ETF alternatives", value=bool(settings.get("include_etfs", True)))
        show_beginner = st.checkbox("Show beginner explanations by default", value=bool(settings.get("show_beginner_explanations", True)))
        show_advanced = st.checkbox("Show advanced metrics", value=bool(settings.get("show_advanced_metrics", False)))
        preferred_sectors = st.text_input("Preferred sectors, comma-separated", value=", ".join(settings.get("preferred_sectors", [])))
        excluded_sectors = st.text_input("Excluded sectors, comma-separated", value=", ".join(settings.get("excluded_sectors", [])))
        submitted = st.form_submit_button("Save settings")

    if submitted:
        updated = DEFAULT_SETTINGS.copy()
        updated.update(settings)
        updated.update(
            {
                "market_universe": market_universe,
                "short_term_risk_tolerance": short_term_risk,
                "long_term_risk_tolerance": long_term_risk,
                "valuation_sensitivity": valuation_sensitivity,
                "minimum_market_cap": int(minimum_market_cap),
                "maximum_risk_score": int(maximum_risk_score),
                "buy_threshold": int(buy_threshold),
                "watch_threshold": int(watch_threshold),
                "include_etfs": include_etfs,
                "show_beginner_explanations": show_beginner,
                "show_advanced_metrics": show_advanced,
                "preferred_sectors": [s.strip() for s in preferred_sectors.split(",") if s.strip()],
                "excluded_sectors": [s.strip() for s in excluded_sectors.split(",") if s.strip()],
            }
        )
        save_settings(updated)
        st.success("Settings saved.")
        st.rerun()

    st.subheader("Daily email overview")
    with st.spinner("Preparing email preview..."):
        scored = get_scored_watchlist()
    top_n = int(settings.get("email_top_n", 5))
    digest_body = build_digest_text(scored, top_n=top_n)
    st.text_area("Email preview", digest_body, height=260)
    with st.form("email_form"):
        recipient = st.text_input("Recipient email", value=settings.get("email_recipient", ""))
        email_enabled = st.checkbox("Enable daily digest setting", value=bool(settings.get("email_daily_digest_enabled", False)))
        email_top_n = st.slider("Number of top ideas to include", 1, 20, top_n)
        save_email = st.form_submit_button("Save email settings")
    if save_email:
        updated = DEFAULT_SETTINGS.copy()
        updated.update(settings)
        updated.update({"email_recipient": recipient.strip(), "email_daily_digest_enabled": email_enabled, "email_top_n": int(email_top_n)})
        save_settings(updated)
        st.success("Email settings saved.")
        st.rerun()

elif page.startswith("?"):
    st.markdown("## Help")
    render_disclaimer(compact=False)
    st.markdown(
        """
        ### How to use the MapleLeaf Investor dashboard
        1. Start on **Home** or **Watchlist**.
        2. Review the **Daily Market Summary** for market context.
        3. Use the **Smart Watchlist** to sort by Buy Ranking, Growth, Risk, or Valuation.
        4. Select a stock to update the detail panel.
        5. Read the analyst-style summary, valuation estimate, earnings highlights, and risk notes.
        6. Use the Education page to learn what each indicator means.
        """
    )

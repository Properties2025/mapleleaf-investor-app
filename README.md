# MapleLeaf Investor App Prototype v4

This version rebuilds the Streamlit app around the supplied MapleLeaf Investor interface concept.

## What changed in v4

- MapleLeaf Investor visual identity and left navigation rail
- Daily Market Summary header with Canadian/U.S. market context
- Smart Watchlist panel inspired by the supplied concept
- Buy Ranking-first sortable table
- Selected-stock detail workspace with:
  - quote header
  - overview tabs
  - price chart panel
  - analyst-style summary
  - intrinsic value estimate
  - dividend highlights placeholder
  - earnings highlights
  - indicator education tiles
- Preserves the v2/v3 data layer, scoring layer, email digest module, cache, and mock fallback

## Important disclaimer

This app is for personal investing research and education only. It does not execute trades. Any Buy Candidate / Watch / Avoid output is a prototype research signal, not financial advice or a guaranteed outcome.

## Install and run on Windows PowerShell

From the extracted app folder that contains `app.py` and `requirements.txt`:

```powershell
python -m venv .venv
.venv\Scripts\Activate.ps1
pip install -r requirements.txt
streamlit run app.py
```

If PowerShell blocks activation, run this once:

```powershell
Set-ExecutionPolicy -Scope CurrentUser -ExecutionPolicy RemoteSigned
.venv\Scripts\Activate.ps1
```

## Folder structure

```text
growth_stock_research_app_v4_mapleleaf/
├── app.py
├── send_daily_digest.py
├── requirements.txt
├── README.md
├── data/
├── src/
│   ├── config.py
│   ├── data_provider.py
│   ├── email_digest.py
│   ├── explainers.py
│   ├── market_summary.py
│   ├── models.py
│   ├── sample_data.py
│   ├── scoring.py
│   ├── storage.py
│   └── ui_components.py
└── tests/
```

## Notes

Live market data depends on internet access and yfinance availability. If live data fails, the app uses mock fallback data so the UI still loads.

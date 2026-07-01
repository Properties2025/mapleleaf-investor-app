from __future__ import annotations
import json, sqlite3
from datetime import datetime, timezone
from pathlib import Path
from typing import Any
from .config import DEFAULT_SETTINGS, WATCHLIST_DEFAULT

PROJECT_ROOT = Path(__file__).resolve().parents[1]
DATA_DIR = PROJECT_ROOT / "data"
SETTINGS_PATH = DATA_DIR / "user_settings.json"
WATCHLIST_PATH = DATA_DIR / "watchlist.json"
CACHE_DB_PATH = DATA_DIR / "cache.sqlite"

def ensure_data_dir() -> None:
    DATA_DIR.mkdir(parents=True, exist_ok=True)

def load_settings() -> dict[str, Any]:
    ensure_data_dir()
    if not SETTINGS_PATH.exists():
        save_settings(DEFAULT_SETTINGS)
        return DEFAULT_SETTINGS.copy()
    try:
        loaded = json.loads(SETTINGS_PATH.read_text(encoding="utf-8"))
    except json.JSONDecodeError:
        return DEFAULT_SETTINGS.copy()
    merged = DEFAULT_SETTINGS.copy()
    merged.update(loaded)
    return merged

def save_settings(settings: dict[str, Any]) -> None:
    ensure_data_dir()
    SETTINGS_PATH.write_text(json.dumps(settings, indent=2), encoding="utf-8")

def load_watchlist() -> list[str]:
    ensure_data_dir()
    if not WATCHLIST_PATH.exists():
        save_watchlist(WATCHLIST_DEFAULT)
        return WATCHLIST_DEFAULT.copy()
    try:
        tickers = json.loads(WATCHLIST_PATH.read_text(encoding="utf-8"))
    except json.JSONDecodeError:
        tickers = WATCHLIST_DEFAULT.copy()
    return sorted({str(t).upper().strip() for t in tickers if str(t).strip()})

def save_watchlist(tickers: list[str]) -> None:
    ensure_data_dir()
    clean = sorted({str(t).upper().strip() for t in tickers if str(t).strip()})
    WATCHLIST_PATH.write_text(json.dumps(clean, indent=2), encoding="utf-8")

def get_connection() -> sqlite3.Connection:
    ensure_data_dir()
    conn = sqlite3.connect(CACHE_DB_PATH)
    conn.execute("""
        CREATE TABLE IF NOT EXISTS ticker_cache (
            ticker TEXT PRIMARY KEY,
            payload TEXT NOT NULL,
            cached_at TEXT NOT NULL
        )
    """)
    return conn

def cache_snapshot(ticker: str, payload: dict[str, Any]) -> None:
    with get_connection() as conn:
        conn.execute(
            "REPLACE INTO ticker_cache (ticker, payload, cached_at) VALUES (?, ?, ?)",
            (ticker.upper(), json.dumps(payload, default=str), datetime.now(timezone.utc).isoformat()),
        )

def read_cached_snapshot(ticker: str) -> tuple[dict[str, Any], datetime] | None:
    with get_connection() as conn:
        row = conn.execute("SELECT payload, cached_at FROM ticker_cache WHERE ticker = ?", (ticker.upper(),)).fetchone()
    if not row:
        return None
    return json.loads(row[0]), datetime.fromisoformat(row[1])

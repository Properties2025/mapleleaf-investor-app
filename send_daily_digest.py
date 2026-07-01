from __future__ import annotations
from datetime import date
from src.data_provider import fetch_many_snapshots
from src.email_digest import build_digest_text, send_digest_email
from src.scoring import score_stock
from src.storage import load_settings, load_watchlist

def main() -> None:
    settings = load_settings()
    recipient = settings.get("email_recipient", "")
    if not recipient:
        raise SystemExit("No email recipient set. Add one in the app Settings tab first.")
    top_n = int(settings.get("email_top_n", 5))
    snapshots = fetch_many_snapshots(load_watchlist())
    scored = [(snapshot, score_stock(snapshot, settings)) for snapshot in snapshots]
    body = build_digest_text(scored, top_n=top_n)
    subject = f"Daily Stock Research Digest — {date.today().isoformat()}"
    send_digest_email(recipient=recipient, subject=subject, body=body)
    print(f"Digest sent to {recipient}")

if __name__ == "__main__":
    main()

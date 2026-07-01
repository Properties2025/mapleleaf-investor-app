from __future__ import annotations
import os, smtplib
from datetime import date
from email.message import EmailMessage

def build_recommendation_rows(scored_items: list[tuple[dict, dict]], top_n: int = 5) -> list[dict]:
    rows = []
    for snapshot, score in scored_items:
        rows.append({
            "Ticker": snapshot.get("ticker"),
            "Company": snapshot.get("company_name"),
            "Rating": score.get("rating"),
            "Buy Score": score.get("buy_score"),
            "Growth": score.get("growth_score"),
            "Risk": score.get("risk_score"),
            "Valuation": score.get("valuation_score"),
            "Momentum": score.get("momentum_score"),
            "Reason": score.get("reason"),
            "Main Risk": score.get("main_risk"),
            "Next Step": score.get("next_step"),
        })
    return sorted(rows, key=lambda row: row.get("Buy Score") or 0, reverse=True)[:top_n]

def build_digest_text(scored_items: list[tuple[dict, dict]], top_n: int = 5) -> str:
    rows = build_recommendation_rows(scored_items, top_n=top_n)
    lines = [
        f"Daily Stock Research Digest — {date.today().isoformat()}",
        "",
        "Research tool only: these are prototype research signals, not financial advice or trade instructions.",
        "",
        f"Top {len(rows)} ranked watchlist ideas:",
        "",
    ]
    for idx, row in enumerate(rows, start=1):
        lines.extend([
            f"{idx}. {row['Ticker']} — {row['Company']}",
            f"   Rating: {row['Rating']} | Buy Score: {row['Buy Score']}/100",
            f"   Scores: Growth {row['Growth']}, Risk {row['Risk']}, Valuation {row['Valuation']}, Momentum {row['Momentum']}",
            f"   Why: {row['Reason']}",
            f"   Main risk: {row['Main Risk']}",
            f"   Next step: {row['Next Step']}",
            "",
        ])
    return "\n".join(lines)

def send_digest_email(
    recipient: str, subject: str, body: str,
    smtp_host: str | None = None, smtp_port: int | None = None,
    smtp_user: str | None = None, smtp_password: str | None = None,
    sender: str | None = None, use_tls: bool = True,
) -> None:
    smtp_host = smtp_host or os.getenv("STOCK_APP_SMTP_HOST", "")
    smtp_port = int(smtp_port or os.getenv("STOCK_APP_SMTP_PORT", "587"))
    smtp_user = smtp_user or os.getenv("STOCK_APP_SMTP_USER", "")
    smtp_password = smtp_password or os.getenv("STOCK_APP_SMTP_PASSWORD", "")
    sender = sender or os.getenv("STOCK_APP_EMAIL_SENDER", smtp_user)
    missing = [name for name, value in {
        "recipient": recipient, "smtp_host": smtp_host, "smtp_user": smtp_user,
        "smtp_password": smtp_password, "sender": sender
    }.items() if not value]
    if missing:
        raise ValueError(f"Missing email configuration: {', '.join(missing)}")
    msg = EmailMessage()
    msg["Subject"], msg["From"], msg["To"] = subject, sender, recipient
    msg.set_content(body)
    with smtplib.SMTP(smtp_host, smtp_port, timeout=30) as server:
        if use_tls:
            server.starttls()
        server.login(smtp_user, smtp_password)
        server.send_message(msg)

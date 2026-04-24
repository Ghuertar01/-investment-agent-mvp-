from datetime import datetime
from pathlib import Path


def build_report_payload(settings: dict, macro: list, news: list, reddit: list, rss: list, sec: list) -> dict:
    return {
        "generated_at": datetime.now().isoformat(timespec="seconds"),
        "portfolio_context": settings["config"].get("portfolio_context", {}),
        "watchlist": settings["config"].get("watchlist", {}),
        "data": {
            "macro": macro,
            "news": news,
            "reddit_osint": reddit,
            "rss_official": rss,
            "sec_filings": sec,
        },
    }


def save_report(settings: dict, markdown_text: str) -> Path:
    reports_dir = Path(settings["env"].get("REPORTS_DIR", "reports"))
    reports_dir.mkdir(parents=True, exist_ok=True)

    filename = f"daily-investment-brief-{datetime.now().strftime('%Y-%m-%d')}.md"
    path = reports_dir / filename
    path.write_text(markdown_text, encoding="utf-8")
    return path

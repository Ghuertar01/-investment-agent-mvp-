from datetime import datetime

from src.config import load_settings
from src.sources.fred import fetch_fred_series
from src.sources.news import fetch_news
from src.sources.reddit import fetch_reddit_posts
from src.sources.rss import fetch_rss_items
from src.sources.sec import fetch_sec_recent_filings
from src.report import build_report_payload, save_report
from src.llm import generate_daily_brief
from src.email_sender import send_email


def main():
    settings = load_settings()

    print("Collecting macro data...")
    macro_data = fetch_fred_series(settings)

    print("Collecting news...")
    news_data = fetch_news(settings)

    print("Collecting Reddit OSINT...")
    reddit_data = fetch_reddit_posts(settings)

    print("Collecting RSS feeds...")
    rss_data = fetch_rss_items(settings)

    print("Collecting SEC filings...")
    sec_data = fetch_sec_recent_filings(settings)

    payload = build_report_payload(
        settings=settings,
        macro=macro_data,
        news=news_data,
        reddit=reddit_data,
        rss=rss_data,
        sec=sec_data,
    )

    print("Generating Daily Investment Brief...")
    brief = generate_daily_brief(settings, payload)

    report_path = save_report(settings, brief)
    print(f"Report saved to: {report_path}")

    if settings["env"].get("SEND_EMAIL", "false").lower() == "true":
        subject = f"Daily Investment Brief — {datetime.now().strftime('%Y-%m-%d')}"
        send_email(settings, subject=subject, markdown_body=brief)
        print("Email sent.")
    else:
        print("SEND_EMAIL=false, email not sent.")


if __name__ == "__main__":
    main()

import os
from pathlib import Path

import yaml
from dotenv import load_dotenv


def load_settings(config_path: str = "config.yaml") -> dict:
    load_dotenv()

    with open(config_path, "r", encoding="utf-8") as f:
        config = yaml.safe_load(f)

    env = {
        "OPENAI_API_KEY": os.getenv("OPENAI_API_KEY", ""),
        "OPENAI_MODEL": os.getenv("OPENAI_MODEL", "gpt-4o-mini"),
        "FRED_API_KEY": os.getenv("FRED_API_KEY", ""),
        "NEWS_API_KEY": os.getenv("NEWS_API_KEY", ""),
        "REDDIT_CLIENT_ID": os.getenv("REDDIT_CLIENT_ID", ""),
        "REDDIT_CLIENT_SECRET": os.getenv("REDDIT_CLIENT_SECRET", ""),
        "REDDIT_USER_AGENT": os.getenv("REDDIT_USER_AGENT", "investment-agent-mvp/0.1"),
        "SEND_EMAIL": os.getenv("SEND_EMAIL", "false"),
        "EMAIL_FROM": os.getenv("EMAIL_FROM", ""),
        "EMAIL_TO": os.getenv("EMAIL_TO", ""),
        "SMTP_HOST": os.getenv("SMTP_HOST", "smtp.gmail.com"),
        "SMTP_PORT": os.getenv("SMTP_PORT", "587"),
        "SMTP_USER": os.getenv("SMTP_USER", ""),
        "SMTP_PASSWORD": os.getenv("SMTP_PASSWORD", ""),
        "REPORTS_DIR": os.getenv("REPORTS_DIR", "reports"),
    }

    Path(env["REPORTS_DIR"]).mkdir(parents=True, exist_ok=True)

    return {"config": config, "env": env}

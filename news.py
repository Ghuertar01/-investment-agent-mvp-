import requests


def fetch_news(settings: dict) -> list[dict]:
    api_key = settings["env"].get("NEWS_API_KEY")
    cfg = settings["config"].get("news", {})

    if not api_key:
        return [{"source": "NewsAPI", "warning": "NEWS_API_KEY not configured"}]

    url = "https://newsapi.org/v2/everything"
    params = {
        "q": cfg.get("query", "markets OR stocks OR Federal Reserve"),
        "language": cfg.get("language", "en"),
        "pageSize": cfg.get("page_size", 20),
        "sortBy": cfg.get("sort_by", "publishedAt"),
        "apiKey": api_key,
    }

    try:
        resp = requests.get(url, params=params, timeout=20)
        resp.raise_for_status()
        articles = resp.json().get("articles", [])
        return [
            {
                "source": "NewsAPI",
                "title": a.get("title"),
                "publisher": (a.get("source") or {}).get("name"),
                "published_at": a.get("publishedAt"),
                "url": a.get("url"),
                "description": a.get("description"),
            }
            for a in articles
        ]
    except Exception as e:
        return [{"source": "NewsAPI", "error": str(e)}]

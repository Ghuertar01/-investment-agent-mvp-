import feedparser


def fetch_rss_items(settings: dict) -> list[dict]:
    feeds = settings["config"].get("rss_feeds", [])
    items = []

    for feed in feeds:
        try:
            parsed = feedparser.parse(feed["url"])
            for entry in parsed.entries[:10]:
                items.append({
                    "source": "RSS",
                    "feed_name": feed["name"],
                    "title": entry.get("title"),
                    "published": entry.get("published"),
                    "url": entry.get("link"),
                    "summary": entry.get("summary", "")[:1000],
                })
        except Exception as e:
            items.append({"source": "RSS", "feed_name": feed.get("name"), "error": str(e)})

    return items

def fetch_reddit_posts(settings: dict) -> list[dict]:
    client_id = settings["env"].get("REDDIT_CLIENT_ID")
    client_secret = settings["env"].get("REDDIT_CLIENT_SECRET")
    user_agent = settings["env"].get("REDDIT_USER_AGENT")
    cfg = settings["config"].get("reddit", {})

    if not client_id or not client_secret:
        return [{"source": "Reddit", "warning": "Reddit credentials not configured"}]

    try:
        import praw

        reddit = praw.Reddit(
            client_id=client_id,
            client_secret=client_secret,
            user_agent=user_agent,
        )

        posts = []
        for subreddit_name in cfg.get("subreddits", []):
            subreddit = reddit.subreddit(subreddit_name)
            for post in subreddit.hot(limit=cfg.get("limit_per_subreddit", 10)):
                if post.score < cfg.get("min_score", 0):
                    continue

                posts.append({
                    "source": "Reddit",
                    "subreddit": subreddit_name,
                    "title": post.title,
                    "score": post.score,
                    "num_comments": post.num_comments,
                    "created_utc": post.created_utc,
                    "url": f"https://www.reddit.com{post.permalink}",
                    "selftext": (post.selftext or "")[:1000],
                })

        return posts

    except Exception as e:
        return [{"source": "Reddit", "error": str(e)}]

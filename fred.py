from datetime import datetime, timedelta
import requests


def fetch_fred_series(settings: dict) -> list[dict]:
    api_key = settings["env"].get("FRED_API_KEY")
    series_config = settings["config"].get("macro", {}).get("fred_series", [])

    if not api_key:
        return [{"source": "FRED", "warning": "FRED_API_KEY not configured"}]

    results = []
    start_date = (datetime.utcnow() - timedelta(days=120)).strftime("%Y-%m-%d")

    for series in series_config:
        series_id = series["id"]
        url = "https://api.stlouisfed.org/fred/series/observations"
        params = {
            "series_id": series_id,
            "api_key": api_key,
            "file_type": "json",
            "observation_start": start_date,
            "sort_order": "desc",
            "limit": 5,
        }

        try:
            resp = requests.get(url, params=params, timeout=20)
            resp.raise_for_status()
            data = resp.json()
            observations = data.get("observations", [])
            latest_valid = next((o for o in observations if o.get("value") not in (".", None)), None)

            results.append({
                "source": "FRED",
                "series_id": series_id,
                "label": series.get("label", series_id),
                "latest": latest_valid,
                "recent_observations": observations[:5],
            })
        except Exception as e:
            results.append({"source": "FRED", "series_id": series_id, "error": str(e)})

    return results

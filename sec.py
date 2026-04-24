import requests


def fetch_sec_recent_filings(settings: dict) -> list[dict]:
    watchlist = settings["config"].get("watchlist", {}).get("equities", [])
    headers = {"User-Agent": "investment-agent-mvp contact@example.com"}

    results = []
    for asset in watchlist:
        cik = asset.get("cik")
        if not cik:
            continue

        cik_padded = str(cik).zfill(10)
        url = f"https://data.sec.gov/submissions/CIK{cik_padded}.json"

        try:
            resp = requests.get(url, headers=headers, timeout=20)
            resp.raise_for_status()
            data = resp.json()
            recent = data.get("filings", {}).get("recent", {})

            filings = []
            for form, date, acc, doc in zip(
                recent.get("form", [])[:10],
                recent.get("filingDate", [])[:10],
                recent.get("accessionNumber", [])[:10],
                recent.get("primaryDocument", [])[:10],
            ):
                acc_no_dash = acc.replace("-", "")
                filings.append({
                    "form": form,
                    "filing_date": date,
                    "accession_number": acc,
                    "url": f"https://www.sec.gov/Archives/edgar/data/{int(cik)}/{acc_no_dash}/{doc}",
                })

            results.append({
                "source": "SEC EDGAR",
                "ticker": asset.get("ticker"),
                "name": asset.get("name"),
                "cik": cik,
                "recent_filings": filings,
            })
        except Exception as e:
            results.append({
                "source": "SEC EDGAR",
                "ticker": asset.get("ticker"),
                "name": asset.get("name"),
                "error": str(e),
            })

    return results

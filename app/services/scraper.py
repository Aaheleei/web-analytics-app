import urllib.parse
from datetime import datetime, timedelta
import feedparser
import requests


def fetch_google_news(show_title: str):
    """Fetches real-time news headlines and publisher information via Google News RSS."""
    query = f'"{show_title}" AND (trailer OR series OR movie OR release OR season)'
    encoded_query = urllib.parse.quote(query)
    rss_url = f"https://news.google.com/rss/search?q={encoded_query}&hl=en-US&gl=US&ceid=US:en"

    feed = feedparser.parse(rss_url)

    scraped_data = []
    seen_titles = set()

    for entry in feed.entries:
        title = entry.get("title", "")
        link = entry.get("link", "")
        published = entry.get("published", "")

        # Extract publisher (Google News formats titles as "Headline - Publisher")
        publisher = "Unknown Outlet"
        if " - " in title:
            parts = title.rsplit(" - ", 1)
            headline_text = parts[0]
            publisher = parts[1]
        else:
            headline_text = title

        if headline_text.lower() not in seen_titles:
            seen_titles.add(headline_text.lower())
            scraped_data.append(
                {
                    "headline": headline_text,
                    "publisher": publisher,
                    "link": link,
                    "published": published,
                }
            )

    return scraped_data


def fetch_wikipedia_pageviews(show_title: str):
    """Fetches real 30-day daily pageviews from Wikimedia's official REST API."""
    formatted_title = show_title.strip().replace(" ", "_")

    end_date = datetime.now()
    start_date = end_date - timedelta(days=30)

    start_str = start_date.strftime("%Y%m%d")
    end_str = end_date.strftime("%Y%m%d")

    url = (
        f"https://wikimedia.org/api/rest_v1/metrics/pageviews/per-article/"
        f"en.wikipedia/all-access/user/{formatted_title}/daily/{start_str}/{end_str}"
    )

    headers = {
        "User-Agent": "OTT-Analytics-Dashboard/1.0 (contact@example.com)"
    }

    try:
        response = requests.get(url, headers=headers, timeout=5)
        if response.status_code == 200:
            data = response.json()
            items = data.get("items", [])
            views_list = [
                {
                    "date": datetime.strptime(
                        item["timestamp"][:8], "%Y%m%d"
                    ).strftime("%Y-%m-%d"),
                    "views": item["views"],
                }
                for item in items
            ]
            return views_list
    except Exception as e:
        print(f"Error fetching Wikipedia pageviews: {e}")

    return []


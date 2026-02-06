import os
from datetime import datetime, timedelta
import json
import urllib.parse
import urllib.request
from dotenv import load_dotenv

# Load environment variables
load_dotenv()
API_KEY = os.getenv("GNEWS_API_KEY")


def gnews_search(q: str, from_: str | None = None, max: int = 10, **kwargs):
    """Query GNews Search API.

    Note: `from` is a keyword in Python, so the function argument uses `from_`.
    If you need to pass a key named `from` via kwargs, use: gnews_search(q, **{"from": "..."}).

    Args:
        q: Query keywords.
        from_: Start time (UTC ISO-8601), e.g., "2026-01-22T00:00:00Z".
        max: Maximum number of results.

    Returns:
        List of articles (with slight field normalization).
    """

    # Compatibility for passing `from` via kwargs (since `from` cannot be a Python parameter name)
    if from_ is None and "from" in kwargs:
        from_ = kwargs.pop("from")

    if kwargs:
        unexpected = ", ".join(sorted(kwargs.keys()))
        raise TypeError(f"Unexpected keyword arguments: {unexpected}")

    if not API_KEY:
        raise ValueError(
            "Missing environment variable GNEWS_API_KEY (can be set in .env or system environment variables)."
        )

    params = {
        "q": q,
        "lang": "en",
        "max": int(max),
        "sortby": "relevance",
        # Common usage for GNews v4 is apikey=...
        "apikey": API_KEY,
    }
    if from_:
        params["from"] = from_

    url = "https://gnews.io/api/v4/search?" + urllib.parse.urlencode(params)

    try:
        with urllib.request.urlopen(url, timeout=20) as response:
            data = json.loads(response.read().decode("utf-8"))

        articles = data.get("articles", []) or []

        results = []
        for article in articles:
            content = article.get("content") or ""
            results.append(
                {
                    "title": article.get("title"),
                    "description": article.get("description"),
                    "source": (article.get("source") or {}).get("name"),
                    "published": article.get("publishedAt"),
                    "url": article.get("url"),
                    "content": (content[:200] + "...") if len(content) > 200 else content,
                }
            )

        return results

    except Exception as e:
        print(f"Error fetching news: {str(e)}")
        return []


def gnews_top_headlines(
    category: str = "general", from_: str | None = None, max: int = 10, **kwargs
):
    """Get GNews Top Headlines.

    Args:
        category: News category, e.g., "general", "world", "nation", "business", "technology",
            "entertainment", "sports", "science", "health".
        from_: Start time (UTC ISO-8601), e.g., "2026-01-22T00:00:00Z".
        max: Maximum number of results.

    Returns:
        List of articles (field structure consistent with gnews_search).
    """

    # Compatibility for passing `from` via kwargs (since `from` cannot be a Python parameter name)
    if from_ is None and "from" in kwargs:
        from_ = kwargs.pop("from")

    if kwargs:
        unexpected = ", ".join(sorted(kwargs.keys()))
        raise TypeError(f"Unexpected keyword arguments: {unexpected}")

    if not API_KEY:
        raise ValueError(
            "Missing environment variable GNEWS_API_KEY (can be set in .env or system environment variables)."
        )

    params = {
        "category": category,
        "lang": "en",
        "country": "us",
        "max": int(max),
        "apikey": API_KEY,
    }
    if from_:
        params["from"] = from_

    url = "https://gnews.io/api/v4/top-headlines?" + urllib.parse.urlencode(params)

    try:
        with urllib.request.urlopen(url, timeout=20) as response:
            data = json.loads(response.read().decode("utf-8"))

        articles = data.get("articles", []) or []

        results = []
        for article in articles:
            content = article.get("content") or ""
            results.append(
                {
                    "title": article.get("title"),
                    "description": article.get("description"),
                    "source": (article.get("source") or {}).get("name"),
                    "published": article.get("publishedAt"),
                    "url": article.get("url"),
                    "content": (content[:200] + "...") if len(content) > 200 else content,
                }
            )

        return results

    except Exception as e:
        print(f"Error fetching news: {str(e)}")
        return []


def get_geo_news(
        time_range = (datetime.now() - timedelta(hours=24)).strftime('%Y-%m-%dT%H:%M:%SZ')
    ):
    """Compatible with old function name: defaults to querying 'place', using time_range as from."""

    keywords = "place OR location OR map OR geospatial OR geography OR geoinformatics OR GIS OR spatial"
    return gnews_search(q=keywords, from_=time_range, max=10)


def get_default_headlines():
    time_range = (datetime.now() - timedelta(hours=36)).strftime('%Y-%m-%dT%H:%M:%SZ')

    max_count = 15
    # select from general, world, nation, business, technology, entertainment, sports, science and health
    categories = ["world", "general", "nation", "business", "technology", "entertainment", "sports", "science", "health"]

    headlines = []
    for category in categories:
        cat_headlines = gnews_top_headlines(category=category, from_=time_range, max=max_count)
        headlines.extend(cat_headlines)
    # Remove duplicates
    seen_urls = set()
    unique_headlines = []
    for item in headlines:
        if item['url'] not in seen_urls:
            unique_headlines.append(item)
            seen_urls.add(item['url'])
    return unique_headlines


# Example usage
if __name__ == "__main__":

    time_range = (datetime.now() - timedelta(hours=24)).strftime('%Y-%m-%dT%H:%M:%SZ')
    news = gnews_search(q="place", from_=time_range, max=10)
    print("## GeoNews from {time_range}\n".format(time_range=time_range))

    if not news:
        print("No related news found.")
    else:
        # Print news list
        for idx, item in enumerate(news, 1):
            print(f"{idx}. [{item['source']}] {item['title']}")
            if item.get("description"):
                print(f"   {item['description']}")
            print(f"   {item['published']}")
            print(f"   {item['url']}\n")

    # Top Headlines Example
    headlines = gnews_top_headlines(category="world", from_=time_range, max=10)
    print("## Top Headlines (world)\n")
    if not headlines:
        print("No related news found.")
    else:
        for idx, item in enumerate(headlines, 1):
            print(f"{idx}. [{item['source']}] {item['title']}")
            if item.get("description"):
                print(f"   {item['description']}")
            print(f"   {item['published']}")
            print(f"   {item['url']}\n")

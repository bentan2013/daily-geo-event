import os
from datetime import datetime, timedelta
import json
import urllib.parse
import urllib.request
from dotenv import load_dotenv

# 加载环境变量
load_dotenv()
API_KEY = os.getenv("GNEWS_API_KEY")


def gnews_search(q: str, from_: str | None = None, max: int = 10, **kwargs):
    """GNews Search API 查询。

    说明：`from` 在 Python 里是关键字，函数形参使用 `from_`。
    如需按用例传入名为 `from` 的键，可用：gnews_search(q, **{"from": "..."}).

    Args:
        q: 查询关键词。
        from_: 起始时间（UTC ISO-8601），例如 "2026-01-22T00:00:00Z"。
        max: 最大返回条数。

    Returns:
        文章列表（做了轻度字段归一化）。
    """

    # 兼容通过 kwargs 传入 `from`（因为 `from` 不能作为 Python 形参名）
    if from_ is None and "from" in kwargs:
        from_ = kwargs.pop("from")

    if kwargs:
        unexpected = ", ".join(sorted(kwargs.keys()))
        raise TypeError(f"Unexpected keyword arguments: {unexpected}")

    if not API_KEY:
        raise ValueError(
            "缺少环境变量 GNEWS_API_KEY（可放到 .env 或系统环境变量中）。"
        )

    params = {
        "q": q,
        "lang": "en",
        "max": int(max),
        "sortby": "relevance",
        # GNews v4 常见用法是 apikey=...
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
        print(f"获取新闻时出错：{str(e)}")
        return []


def gnews_top_headlines(
    category: str = "general", from_: str | None = None, max: int = 10, **kwargs
):
    """获取 GNews Top Headlines。

    Args:
        category: 新闻分类，例如 "general", "world", "nation", "business", "technology",
            "entertainment", "sports", "science", "health"。
        from_: 起始时间（UTC ISO-8601），例如 "2026-01-22T00:00:00Z"。
        max: 最大返回条数。

    Returns:
        文章列表（字段结构与 gnews_search 基本一致）。
    """

    # 兼容通过 kwargs 传入 `from`（因为 `from` 不能作为 Python 形参名）
    if from_ is None and "from" in kwargs:
        from_ = kwargs.pop("from")

    if kwargs:
        unexpected = ", ".join(sorted(kwargs.keys()))
        raise TypeError(f"Unexpected keyword arguments: {unexpected}")

    if not API_KEY:
        raise ValueError(
            "缺少环境变量 GNEWS_API_KEY（可放到 .env 或系统环境变量中）。"
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
        print(f"获取新闻时出错：{str(e)}")
        return []


def get_geo_news(
        time_range = (datetime.now() - timedelta(hours=24)).strftime('%Y-%m-%dT%H:%M:%SZ')
    ):
    """兼容旧函数名：默认查询 place，并传入 time_range 作为 from。"""

    keywords = "place OR location OR map OR geospatial OR geography OR geoinformatics OR GIS OR spatial"
    return gnews_search(q=keywords, from_=time_range, max=10)

# 示例使用
if __name__ == "__main__":

    time_range = (datetime.now() - timedelta(hours=24)).strftime('%Y-%m-%dT%H:%M:%SZ')
    news = gnews_search(q="place", from_=time_range, max=10)
    print("## GeoNews from {time_range}\n".format(time_range=time_range))

    if not news:
        print("没有找到相关的新闻。")
    else:
        # 打印新闻列表
        for idx, item in enumerate(news, 1):
            print(f"{idx}. [{item['source']}] {item['title']}")
            if item.get("description"):
                print(f"   {item['description']}")
            print(f"   {item['published']}")
            print(f"   {item['url']}\n")

    # Top Headlines 示例
    headlines = gnews_top_headlines(category="general", from_=time_range, max=10)
    print("## Top Headlines (general)\n")
    if not headlines:
        print("没有找到相关的新闻。")
    else:
        for idx, item in enumerate(headlines, 1):
            print(f"{idx}. [{item['source']}] {item['title']}")
            if item.get("description"):
                print(f"   {item['description']}")
            print(f"   {item['published']}")
            print(f"   {item['url']}\n")

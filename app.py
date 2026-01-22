from datetime import datetime, timedelta
from gnews_utils import gnews_top_headlines
from geofilter_utils import filter_geo_headlines


def get_default_headlines():
    time_range = (datetime.now() - timedelta(hours=36)).strftime('%Y-%m-%dT%H:%M:%SZ')

    max_count = 15 
    # select from general, world, nation, business, technology, entertainment, sports, science and health
    catagories = ["world", "general", "nation", "business", "technology", "entertainment", "sports", "science", "health"]

    headlines = []
    for category in catagories:
        cat_headlines = gnews_top_headlines(category=category, from_=time_range, max=max_count)
        headlines.extend(cat_headlines)
    # 去重
    seen_urls = set()
    unique_headlines = []
    for item in headlines:
        if item['url'] not in seen_urls:
            unique_headlines.append(item)
            seen_urls.add(item['url'])
    return unique_headlines


if __name__ == "__main__":
    headlines = get_default_headlines()
    geo_headlines = filter_geo_headlines(headlines)
    print("## Geo Related Top Headlines\n")
    if not geo_headlines:
        print("没有找到相关的新闻。")
    else:
        for idx, item in enumerate(geo_headlines, 1):
            print(f"{idx}. [{item['source']}] {item['title']}")
            if item.get("description"):
                print(f"   {item['description']}")
            print(f"   {item['published']}")
            print(f"   {item['url']}\n")



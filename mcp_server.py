from mcp.server.fastmcp import FastMCP
from gnews_utils import get_default_headlines
from geofilter_utils import filter_geo_headlines

mcp = FastMCP("News Agent")

@mcp.tool()
def get_geo_headlines() -> list[dict]:
    """
    Get the latest geo-related news headlines.
    Fetches default headlines from various categories and filters them for geographic relevance.
    """
    headlines = get_default_headlines()
    return filter_geo_headlines(headlines)

if __name__ == "__main__":
    mcp.run()

from datetime import datetime, timedelta
from typing import Optional
from fastapi import FastAPI
from pydantic import BaseModel, Field
import uvicorn

from gnews_utils import gnews_top_headlines, gnews_search, get_default_headlines
from geofilter_utils import filter_geo_headlines

app = FastAPI()

class SearchRequest(BaseModel):
    q: str
    from_: Optional[str] = Field(None, alias="from")
    max: int = 10

class TopHeadlinesRequest(BaseModel):
    category: str = "general"
    from_: Optional[str] = Field(None, alias="from")
    max: int = 10

@app.get("/")
def read_root():
    headlines = get_default_headlines()
    return filter_geo_headlines(headlines)

@app.post("/")
def read_root_post():
    headlines = get_default_headlines()
    return filter_geo_headlines(headlines)

@app.post("/gnews/search")
def search_gnews(request: SearchRequest):
    return gnews_search(q=request.q, from_=request.from_, max=request.max)

@app.post("/gnews/top-headlines")
def top_headlines_gnews(request: TopHeadlinesRequest):
    return gnews_top_headlines(category=request.category, from_=request.from_, max=request.max)

if __name__ == "__main__":
    uvicorn.run("app:app", host="0.0.0.0", port=8000)

# daily-geo-event
Daily Geo-Impact Digest: Tracking Location-Driven News Events

## Install

```bash
uv venv --python=python3.13 --seed
```

Activate (macOS/Linux):

```bash
source .venv/bin/activate
```

```
uv pip install /Users/ben7276/projects/AgenticGIS/gen-ai-toolkit/dist/gen_ai_toolkit-0.9.8-py3-none-any.whl
pip install -r requirements.txt
```

## Running the Service

Start the FastAPI server:

```bash
uvicorn app:app --host 0.0.0.0 --port 8000
```

## API Endpoints

### 1. Default Geo Headlines
Returns a list of deduplicated, geography-related headlines from the last 36 hours.

- **URL:** `/`
- **Method:** `GET` or `POST`
- **Example:**
  ```bash
  curl http://localhost:8000/
  ```

### 2. GNews Search
Search for news articles using keywords.

- **URL:** `/gnews/search`
- **Method:** `POST`
- **Body:**
  ```json
  {
    "q": "keyword",
    "from": "2023-01-01T00:00:00Z",
    "max": 10
  }
  ```
- **Example:**
  ```bash
  curl -X POST "http://localhost:8000/gnews/search" \
       -H "Content-Type: application/json" \
       -d '{"q": "climate change", "max": 5}'
  ```

### 3. GNews Top Headlines
Get top headlines by category.

- **URL:** `/gnews/top-headlines`
- **Method:** `POST`
- **Body:**
  ```json
  {
    "category": "general",
    "from": "2023-01-01T00:00:00Z",
    "max": 10
  }
  ```
- **Categories:** world, general, nation, business, technology, entertainment, sports, science, health
- **Example:**
  ```bash
  curl -X POST "http://localhost:8000/gnews/top-headlines" \
       -H "Content-Type: application/json" \
       -d '{"category": "technology", "max": 5}'
  ```

## MCP Server

This project provides an [MCP (Model Context Protocol)](https://github.com/modelcontextprotocol/python-sdk) server that exposes the geo-headline filtering logic as a tool. This allows other AI agents to directly invoke the news filtering service.

### Deployment

To run the MCP server:

```bash
# Ensure environment variables (GNEWS_API_KEY, AZURE_API_DEPLOYMENT) are set
python mcp_server.py
```

### Usage

The server exposes the following tool:

- **`get_geo_headlines`**: Fetches the latest headlines from various categories (world, general, technology, etc.) and filters them to return only those relevant to geography or geospatial topics.

### Calling from an MCP Client

You can connect to this server using any MCP-compliant client. For example, using the Python SDK:

```python
from mcp.client.stdio import StdioServerParameters, stdio_client
from mcp.client.session import ClientSession

server_params = StdioServerParameters(
    command="python",
    args=["mcp_server.py"],
    env=None # Optional: pass environment variables here if needed
)

async with stdio_client(server_params) as (read, write):
    async with ClientSession(read, write) as session:
        await session.initialize()

        # List tools
        tools = await session.list_tools()
        print(tools)

        # Call the tool
        result = await session.call_tool("get_geo_headlines")
        print(result)
```

## GNews API

https://docs.gnews.io/

GNews API is a REST API service to search articles from over 80,000 worldwide sources. The API provides access to real-time news and historical data, as well as top headlines based on Google News rankings.

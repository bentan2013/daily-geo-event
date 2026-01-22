import os
from typing import Iterable


def construct_geo_filter_instructions_in_en() -> str:
	return (
		"You are a geography expert. From the provided news headlines, "
		"identify and extract only those that are related to geography, "
		"including topics such as places, locations, maps, geospatial data, "
		"geography, geoinformatics, GIS, and spatial analysis, we will use the location or places mentioned in the news for further analysis. "
		"Only return the number of the geo related headlines found. Only numbers should be returned. No additional text."
	)


def construct_geo_headlines_prompt(headlines: Iterable[dict]) -> str:
	prompt = "Select geo related headlines:\n\n"
	for idx, item in enumerate(headlines, 1):
		prompt += f"{idx}. [{item.get('source')}] {item.get('title')}\n"
		if item.get("description"):
			prompt += f"   {item['description']}\n"
		prompt += f"   {item.get('published')}\n"
		prompt += f"   {item.get('url')}\n\n"
	return prompt


def filter_geo_headlines_with_agent(headlines: list[dict], model: str | None = None) -> str:
	"""使用 gait Agent 返回命中的 headline 序号字符串。"""

	from gait import Agent

	if model is None:
		deployment = os.environ.get("AZURE_API_DEPLOYMENT")
		if not deployment:
			raise ValueError("缺少环境变量 AZURE_API_DEPLOYMENT")
		model = "azure/" + deployment

	agent = Agent(model=model, instructions=construct_geo_filter_instructions_in_en())
	response = agent(construct_geo_headlines_prompt(headlines))
	return response.content


def parse_headline_indices(text: str) -> list[int]:
	"""把 Agent 返回的序号文本解析成 int 列表（支持逗号/空格/换行分隔）。"""

	parts = text.replace(",", " ").replace("\n", " ").split()
	return [int(p) for p in parts if p.isdigit()]


def filter_geo_headlines(headlines: list[dict], model: str | None = None) -> list[dict]:
	"""返回被 gait 选中的 geo 相关新闻条目。"""

	no_list_text = filter_geo_headlines_with_agent(headlines, model=model)
	indices = parse_headline_indices(no_list_text)
	return [headlines[i - 1] for i in indices if 1 <= i <= len(headlines)]


import os
from typing import Iterable
from pydantic import BaseModel


class GeoHeadlineSelection(BaseModel):
	indices: list[int]


def construct_geo_filter_instructions_in_en() -> str:
	return (
		"You are a geography expert. From the provided news headlines, "
		"identify and extract only those that are related to geography, "
		"including topics such as places, locations, maps, geospatial data, "
		"geography, geoinformatics, GIS, and spatial analysis, we will use the location or places mentioned in the news for further analysis. "
		"Select the indices of the geo related headlines."
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


def filter_geo_headlines_with_agent(headlines: list[dict], model: str | None = None) -> list[int]:
	"""Return the list of headline indices selected by the gait Agent."""

	from gait import Agent

	if model is None:
		deployment = os.environ.get("AZURE_API_DEPLOYMENT")
		if not deployment:
			raise ValueError("Missing environment variable AZURE_API_DEPLOYMENT")
		model = "azure/" + deployment

	agent = Agent(
		model=model,
		instructions=construct_geo_filter_instructions_in_en(),
		response_format=GeoHeadlineSelection
	)
	response = agent(construct_geo_headlines_prompt(headlines))
	selection = GeoHeadlineSelection.model_validate_json(response.content)
	return selection.indices


def filter_geo_headlines(headlines: list[dict], model: str | None = None) -> list[dict]:
	"""Return geo-related news items selected by gait."""

	indices = filter_geo_headlines_with_agent(headlines, model=model)
	return [headlines[i - 1] for i in indices if 1 <= i <= len(headlines)]

from typing import TypedDict, List, Dict, Optional

class AgentState(TypedDict):
    initial_url: str
    product_json: Dict
    homepage_markdown: str
    links_to_scrape: Dict[str, str]
    scraped_pages_content: Dict[str, str]
    structured_data: Dict
    competitor_urls: Optional[List[str]]

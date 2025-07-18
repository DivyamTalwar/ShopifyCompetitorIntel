import httpx
import re
from firecrawl import FirecrawlApp
from app.core.config import settings
from typing import Dict, Optional

def find_link(markdown_content: str, keywords: list[str]) -> Optional[str]:
    for keyword in keywords:
        match = re.search(rf'\[.*?{re.escape(keyword)}.*?\]\((.*?)\)', markdown_content, re.IGNORECASE)
        if match:
            return match.group(1)
    return None

async def fetch_products_json(url: str):
    async with httpx.AsyncClient() as client:
        try:
            response = await client.get(f"{url}/products.json")
            response.raise_for_status()
            return response.json()
        except httpx.HTTPStatusError as e:
            print(f"HTTP error occurred: {e}")
            return None
        except httpx.RequestError as e:
            print(f"An error occurred while requesting {e.request.url!r}.")
            return None

async def scrape_page_with_firecrawl(url: str):
    app = FirecrawlApp(api_key=settings.FIRECRRAWL_API_KEY)
    try:
        scraped_data = app.scrape_url(url)
        return scraped_data['markdown']
    except Exception as e:
        print(f"An error occurred during scraping: {e}")
        return None

def extract_links_from_markdown(markdown_content: str, base_url: str) -> Dict[str, str]:
    links = {
        "privacy": find_link(markdown_content, ["privacy policy"]),
        "returns": find_link(markdown_content, ["return policy", "refund policy"]),
        "contact": find_link(markdown_content, ["contact us"]),
        "faq": find_link(markdown_content, ["faq", "frequently asked questions"]),
        "blogs": find_link(markdown_content, ["blog", "blogs"]),
        "order_tracking": find_link(markdown_content, ["track your order", "order tracking"]),
    }
    
    for key, link in links.items():
        if link and not link.startswith('http'):
            links[key] = f"{base_url}{link}"
            
    return links

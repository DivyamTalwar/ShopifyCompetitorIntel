from googleapiclient.discovery import build
from app.core.config import settings
from typing import List

def find_competitors(brand_name: str) -> List[str]:
    service = build("customsearch", "v1", developerKey=settings.GOOGLE_API_KEY)
    res = service.cse().list(
        q=f"competitors of {brand_name}",
        cx=settings.GOOGLE_CSE_ID,
    ).execute()
    
    competitor_urls = [item['link'] for item in res.get('items', [])]
    return competitor_urls[:5]

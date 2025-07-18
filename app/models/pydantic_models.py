from pydantic import BaseModel, HttpUrl
from typing import List, Optional, Dict

class WebsiteRequest(BaseModel):
    website_url: HttpUrl

class Product(BaseModel):
    id: int
    title: str
    vendor: str
    price: str

class FAQ(BaseModel):
    question: str
    answer: str

class BrandContext(BaseModel):
    brand_name: str
    about_text: Optional[str]
    contacts: Optional[Dict]
    social_handles: Optional[Dict]
    policies: Optional[Dict]
    faqs: List[FAQ]
    hero_products: List[Product]
    full_product_catalog: List[Product]

class CompetitorAnalysisResponse(BaseModel):
    main_brand: BrandContext
    competitors: List[BrandContext]

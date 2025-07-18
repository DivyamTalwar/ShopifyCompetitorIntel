from langgraph.graph import StateGraph, END
from app.graph.state import AgentState
from app.services import data_extractor, data_structurer
from app.db.session import SessionLocal
from app.models.sql_models import Brand, Competitor
import json

def node_fetch_initial_data(state: AgentState):
    initial_url = state['initial_url']
    product_json = data_extractor.fetch_products_json(initial_url)
    homepage_markdown = data_extractor.scrape_page_with_firecrawl(initial_url)
    return {
        "product_json": product_json,
        "homepage_markdown": homepage_markdown,
    }

def node_identify_key_links(state: AgentState):
    homepage_markdown = state['homepage_markdown']
    base_url = state['initial_url']
    links_to_scrape = data_extractor.extract_links_from_markdown(homepage_markdown, base_url)
    return {"links_to_scrape": links_to_scrape}

def node_scrape_subpages(state: AgentState):
    scraped_pages_content = {}
    for key, url in state['links_to_scrape'].items():
        scraped_pages_content[key] = data_extractor.scrape_page_with_firecrawl(url)
    return {"scraped_pages_content": scraped_pages_content}

def node_structure_all_data(state: AgentState):
    structured_data = {
        "brand_name": state["product_json"]["products"][0]["vendor"],
        "about_text": data_structurer.summarize_about_us(state["homepage_markdown"]),
        "contacts": data_structurer.extract_contact_info(state["scraped_pages_content"].get("contact")),
        "social_handles": data_structurer.extract_social_links(state["homepage_markdown"]),
        "policies": {
            "privacy": state["scraped_pages_content"].get("privacy"),
            "returns": state["scraped_pages_content"].get("returns"),
        },
        "faqs": data_structurer.get_structured_faqs(state["scraped_pages_content"].get("faq")),
        "important_links": {
            "blogs": state["scraped_pages_content"].get("blogs"),
            "order_tracking": state["scraped_pages_content"].get("order_tracking"),
        },
        "hero_products": state["product_json"]["products"][:5],
        "full_product_catalog": state["product_json"]["products"],
    }
    return {"structured_data": structured_data}

def node_persist_data(state: AgentState):
    db = SessionLocal()
    try:
        main_brand_data = state['structured_data']
        
        brand = Brand(**main_brand_data)
        db.add(brand)
        db.commit()
        db.refresh(brand)

        if 'competitors' in state and state['competitors']:
            for comp_data in state['competitors']:
                competitor = Competitor(brand_id=brand.id, **comp_data)
                db.add(competitor)
            db.commit()
    finally:
        db.close()
    
    return {}

def should_continue(state: AgentState):
    if state["links_to_scrape"]:
        return "continue"
    else:
        return "end"

workflow = StateGraph(AgentState)
workflow.add_node("fetch_initial_data", node_fetch_initial_data)
workflow.add_node("identify_key_links", node_identify_key_links)
workflow.add_node("scrape_subpages", node_scrape_subpages)
workflow.add_node("structure_all_data", node_structure_all_data)
workflow.add_node("persist_data", node_persist_data)

workflow.set_entry_point("fetch_initial_data")
workflow.add_edge("fetch_initial_data", "identify_key_links")
workflow.add_conditional_edges(
    "identify_key_links",
    should_continue,
    {
        "continue": "scrape_subpages",
        "end": "structure_all_data",
    },
)
workflow.add_edge("scrape_subpages", "structure_all_data")
workflow.add_edge("structure_all_data", "persist_data")
workflow.add_edge("persist_data", END)

agent = workflow.compile()

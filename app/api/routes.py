from fastapi import APIRouter, HTTPException
from app.models.pydantic_models import WebsiteRequest, CompetitorAnalysisResponse
from app.graph.agent import agent
from app.services import competitor_finder

router = APIRouter()

@router.post("/fetch-insights", response_model=CompetitorAnalysisResponse)
async def fetch_insights(request: WebsiteRequest):
    initial_state = {"initial_url": str(request.website_url)}
    try:
        main_brand_result = agent.invoke(initial_state)
        main_brand_context = main_brand_result['structured_data']

        competitors_urls = competitor_finder.find_competitors(main_brand_context['brand_name'])

        competitor_contexts = []
        for url in competitors_urls:
            competitor_state = {"initial_url": url}
            try:
                competitor_result = agent.invoke(competitor_state)
                competitor_contexts.append(competitor_result['structured_data'])
            except Exception as e:
                print(f"Failed to process competitor {url}: {e}")


        return CompetitorAnalysisResponse(
            main_brand=main_brand_context,
            competitors=competitor_contexts
        )

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

from dotenv import load_dotenv
load_dotenv()
from fastapi import FastAPI
from app.services.scoring import calculate_scores
from app.services.mobile_service import fetch_mobile_data
from app.routes.health import router as health_router
from app.services.ai_service import generate_explanation
from app.services.external_api_service import fetch_external_products
from app.routes.recommendation import router as recommendation_router
from app.services.decision_engine import generate_recommendations
from app.schemas.recommendation import (
    RecommendationRequest,
    RecommendationResponse
)

from fastapi.middleware.cors import CORSMiddleware


app = FastAPI()
app.include_router(health_router)
app.include_router(recommendation_router)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# -------------------------
# Health Check
# -------------------------
@app.get("/")
def root():
    return {"message": "ClariCart API running"}

# -------------------------
# Recommendation API
# -------------------------
@app.post(
    "/recommendations",
    response_model=RecommendationResponse
)
def get_recommendations(
    request: RecommendationRequest
):
    return generate_recommendations(
        request.model_dump()
    )


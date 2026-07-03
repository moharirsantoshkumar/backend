from app.schemas.recommendation import (
    RecommendationResponse,
    Decision
)
from app.services.decision_service import build_decision


def build_response(
    category,
    top_recommendation,
    alternatives,
):

    decision = build_decision(top_recommendation)

    return RecommendationResponse(
        category=category,
        decision=decision,
        top_recommendation=top_recommendation,
        alternatives=alternatives,
    )
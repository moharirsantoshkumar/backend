from pydantic import BaseModel


class PriceHistoryPoint(BaseModel):
    day: int
    price: float


class PriceIntelligence(BaseModel):
    price_history: list[PriceHistoryPoint]
    price_trend: str
    lowest_price: float
    highest_price: float
    average_price: float
    predicted_price: float
    recommended_action: str
    estimated_wait_savings: float
    pricing_confidence: str
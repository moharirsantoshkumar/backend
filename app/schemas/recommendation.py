from pydantic import BaseModel
from typing import Dict, List, Optional


class RecommendationRequest(BaseModel):
    category: str = "laptops"
    weights: Dict[str, float]

class Decision(BaseModel):
    confidence: str
    summary: str
    tradeoff: str
    best_for: str

class Retailer(BaseModel):
    store: str
    price: float
    url: str

class Product(BaseModel):
    id: int
    name: str
    image: str
    brand: str
    price: float
    rating: float
    battery_hours: int
    processor: str
    ram_gb: int
    score: float
    pricing: Pricing | None = None
    retailers: list[Retailer] = []
    verdict: Optional[str] = None
    explanation: Optional[str] = None
    decision_summary: Optional[str] = None
    tradeoff_vs_next: Optional[str] = None
    confidence: Optional[str] = None
    best_for: Optional[str] = None

class Pricing(BaseModel):
    source: str
    currency: str
    best_store: str
    best_price: float
    market_average: float
    potential_savings: float
    buy_recommendation: str

class RecommendationResponse(BaseModel):
    category: str
    decision: Decision
    top_recommendation: Product
    alternatives: List[Product]
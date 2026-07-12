from pydantic import BaseModel


class RetailerScore(BaseModel):
    retailer: str
    score: int
    badge: str
    trust_score: int
    delivery_score: int
    value_score: int


class RetailerIntelligence(BaseModel):
    best_retailer: str
    summary: str
    retailers: list[RetailerScore]
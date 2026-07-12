from pydantic import BaseModel


class BuyingAdvisor(BaseModel):
    decision: str
    deal_score: int
    potential_savings: float
    wait_days: int
    price_risk: str
    next_sale_probability: str
    summary: str
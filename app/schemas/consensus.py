from pydantic import BaseModel


class AIModelOpinion(BaseModel):
    model: str
    recommendation: str
    reasoning: str
    agrees_with_final: bool


class Consensus(BaseModel):
    agreement_score: int
    majority_choice: str
    summary: str
    opinions: list[AIModelOpinion]
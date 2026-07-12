from pydantic import BaseModel


class Confidence(BaseModel):
    score: int
    level: str
    factors: list[str]
    summary: str
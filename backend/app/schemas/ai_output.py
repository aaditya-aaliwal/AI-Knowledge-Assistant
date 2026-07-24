from pydantic import BaseModel


class AIResponseSchema(BaseModel):
    answer: str
    category: str
    confidence: float
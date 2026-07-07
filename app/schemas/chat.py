from pydantic import BaseModel, Field
from datetime import datetime


class ChatCreate(BaseModel):
    title: str = Field(min_length=3, max_length=20)
    user_id: int

class ChatResponse(BaseModel):
    id: int
    title: str = Field(min_length=3, max_length=20)
    user_id: int
    created_at: datetime

    class Config:
        from_attributes = True


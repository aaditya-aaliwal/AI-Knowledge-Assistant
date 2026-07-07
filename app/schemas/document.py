from pydantic import BaseModel, Field
from datetime import datetime


class DocumentCreate(BaseModel):
    filename: str = Field(min_length=3, max_length=20)
    content: str = Field(min_length=3, max_length=1000)
    chat_id: int

class DocumentResponse(BaseModel):
    id: int
    filename: str = Field(min_length=3, max_length=20)
    content: str = Field(min_length=3, max_length=1000)
    chat_id: int
    created_at: datetime

    class Config:
        from_attributes = True

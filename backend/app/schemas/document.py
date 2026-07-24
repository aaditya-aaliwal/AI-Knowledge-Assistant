from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime


class DocumentCreate(BaseModel):
    filename: str = Field(min_length=1, max_length=255)
    content: str = Field(min_length=3, max_length=1000)
    chat_id: int

class DocumentResponse(BaseModel):
    id: int
    filename: str = Field(min_length=1, max_length=255)
    content: str = Field(min_length=3, max_length=1000)
    chat_id: int
    created_at: datetime
    filepath: Optional[str] = None
    uploaded_by: Optional[int] = None
    status: str = "READY"

    class Config:
        from_attributes = True

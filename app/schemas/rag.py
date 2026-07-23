from pydantic import BaseModel, Field


class RAGRequest(BaseModel):
    question: str = Field(
        ...,
        description="User's question to be answered using RAG."
    )


class RAGResponse(BaseModel):
    answer: str = Field(
        ...,
        description="AI-generated answer based on retrieved document context."
    )
    sources: list[str] = Field(
        ...,
        description="List of source documents used to generate the answer."
    )
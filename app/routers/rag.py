from fastapi import APIRouter

from app.schemas.rag import RAGRequest, RAGResponse
from app.services.embedding_service import EmbeddingService
from app.services.rag_service import RAGService
from app.services.retrieval_service import RetrievalService
from app.vectorstore.vector_store import VectorStore


router = APIRouter(
    prefix="/rag",
    tags=["RAG"],
)


embedding_service = EmbeddingService()
vector_store = VectorStore()

retrieval_service = RetrievalService(
    embedding_service=embedding_service,
    vector_store=vector_store,
)

rag_service = RAGService(
    retrieval_service=retrieval_service,
)


@router.post(
    "/ask",
    response_model=RAGResponse,
)
def ask_question(
    request: RAGRequest,
) -> RAGResponse:
    """
    Answer user questions using Retrieval-Augmented Generation (RAG).
    """

    return rag_service.generate_answer(
        question=request.question,
    )
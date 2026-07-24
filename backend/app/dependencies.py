from app.services.chunking_service import ChunkingService
from app.services.document_ingestion_service import DocumentIngestionService
from app.services.embedding_service import EmbeddingService
from app.services.pdf_service import PDFService
from app.services.retrieval_service import RetrievalService
from app.vectorstore.vector_store import VectorStore


def get_app_name():
    return "AI Knowledge Assistant Backend"

def get_pdf_service() -> PDFService:
    return PDFService()


def get_chunking_service() -> ChunkingService:
    return ChunkingService()


def get_embedding_service() -> EmbeddingService:
    return EmbeddingService()


def get_vector_store() -> VectorStore:
    return VectorStore()


def get_document_ingestion_service() -> DocumentIngestionService:
    return DocumentIngestionService(
        pdf_service=get_pdf_service(),
        chunking_service=get_chunking_service(),
        embedding_service=get_embedding_service(),
        vector_store=get_vector_store(),
    )


def get_retrieval_service() -> RetrievalService:
    return RetrievalService(
        embedding_service=get_embedding_service(),
        vector_store=get_vector_store(),
    )
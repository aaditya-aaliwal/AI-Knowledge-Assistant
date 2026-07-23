from pathlib import Path

from app.logger import logger
from app.services.chunking_service import ChunkingService
from app.services.embedding_service import EmbeddingService
from app.services.pdf_service import PDFService
from app.vectorstore.vector_store import VectorStore


class DocumentIngestionService:
    """
    Orchestrates the complete document ingestion pipeline.
    """

    def __init__(
        self,
        pdf_service: PDFService,
        chunking_service: ChunkingService,
        embedding_service: EmbeddingService,
        vector_store: VectorStore,
    ):
        self.pdf_service = pdf_service
        self.chunking_service = chunking_service
        self.embedding_service = embedding_service
        self.vector_store = vector_store

    def ingest_document(
        self,
        file_path: Path
    ) -> None:
        """
        Process a PDF document and store its embeddings in ChromaDB.
        """

        try:
            text = self.pdf_service.extract_text(file_path)

            chunks = self.chunking_service.split_text(text)

            embeddings = self.embedding_service.generate_embeddings(chunks)

            ids = [
                f"{file_path.stem}_chunk_{index}"
                for index, _ in enumerate(chunks)
            ]

            metadatas = [
                {
                    "source": file_path.name,
                    "chunk": index + 1,
                    "total_chunks": len(chunks),
                }
                for index, _ in enumerate(chunks)
            ]

            if not (
                len(ids)
                == len(chunks)
                == len(embeddings)
                == len(metadatas)
            ):
                raise ValueError(
                    "IDs, documents, embeddings, and metadata must have the same length."
                )

            self.vector_store.add_documents(
                ids=ids,
                documents=chunks,
                embeddings=embeddings,
                metadatas=metadatas,
            )

            logger.info(
                f"Successfully ingested document: {file_path.name}"
            )

        except Exception:
            logger.exception(
                f"Failed to ingest document: {file_path.name}"
            )
            raise
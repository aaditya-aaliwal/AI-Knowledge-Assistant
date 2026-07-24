from app.logger import logger
from app.services.embedding_service import EmbeddingService
from app.vectorstore.vector_store import VectorStore


class RetrievalService:
    """
    Handles retrieval of relevant document chunks from the vector database.
    """

    def __init__(
        self,
        embedding_service: EmbeddingService,
        vector_store: VectorStore,
    ):
        self.embedding_service = embedding_service
        self.vector_store = vector_store

    def retrieve(
        self,
        question: str,
    ) -> dict:
        """
        Retrieve the most relevant document chunks for a user question.
        """
        try:
            query_embedding = (
                self.embedding_service.generate_query_embedding(
                    question
                )
            )

            results = self.vector_store.search(
                query_embedding=query_embedding,
            )

            logger.info(
                "Successfully retrieved relevant document chunks."
            )

            return results

        except Exception:
            logger.exception(
                "Failed to retrieve relevant document chunks."
            )
            raise
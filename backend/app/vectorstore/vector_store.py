from app.vectorstore.chroma_client import collection
from app.logger import logger

class VectorStore:
    """
    Handles all vector database operations using ChromaDB.
    """

    def __init__(self):
        self.collection = collection

    def add_documents(
        self,
        ids: list[str],
        documents: list[str],
        embeddings: list[list[float]],
        metadatas: list[dict[str, object]]
    ) -> None:
        """
        Store document chunks, embeddings, and metadata in ChromaDB.
        """
        self.collection.add(
            ids=ids,
            documents=documents,
            embeddings=embeddings,
            metadatas=metadatas,
        )

    def search(
        self,
        query_embedding: list[float],
        top_k: int = 3,
    ) -> dict:
        try:
            results = self.collection.query(
                query_embeddings=[query_embedding],
                n_results=top_k,
            )

            return {
                "documents": results["documents"][0],
                "metadatas": results["metadatas"][0],
                "distances": results["distances"][0],
            }

        except Exception:
            logger.exception(
                "Failed to perform similarity search."
            )
            raise
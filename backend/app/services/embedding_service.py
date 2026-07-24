from langchain_google_genai import GoogleGenerativeAIEmbeddings

from app.config import settings


embedding_model = GoogleGenerativeAIEmbeddings(
    model=settings.GEMINI_EMBEDDING_MODEL,
    google_api_key=settings.GEMINI_API_KEY,
)


class EmbeddingService:

    def __init__(self):
        self.embedding_model = embedding_model

    def generate_embeddings(
        self,
        documents: list[str]
    ) -> list[list[float]]:
        embeddings = self.embedding_model.embed_documents(documents)

        return embeddings
    
    def generate_query_embedding(
        self,
        query: str
    ) -> list[float]:
        embedding = self.embedding_model.embed_query(query)

        return embedding
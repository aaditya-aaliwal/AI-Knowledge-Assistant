from langchain_text_splitters import RecursiveCharacterTextSplitter

from app.config import settings


text_splitter = RecursiveCharacterTextSplitter(
    chunk_size=settings.CHUNK_SIZE,
    chunk_overlap=settings.CHUNK_OVERLAP,
)


class ChunkingService:
    """
    Handles text chunking using LangChain's RecursiveCharacterTextSplitter.
    """

    def __init__(self):
        self.text_splitter = text_splitter

    def split_text(
        self,
        text: str
    ) -> list[str]:
        """
        Split extracted text into smaller chunks for embedding generation.
        """

        if not text or not text.strip():
            raise ValueError("Text cannot be empty.")

        chunks = self.text_splitter.split_text(text)

        return chunks
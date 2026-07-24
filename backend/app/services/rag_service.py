import json

from app.logger import logger
from app.prompts.rag_prompt import RAG_PROMPT
from app.schemas.rag import RAGResponse
from app.services.cache_service import cache_service
from app.services.llm_service import generate_response
from app.services.retrieval_service import RetrievalService


class RAGService:
    """
    Handles Retrieval-Augmented Generation (RAG).

    Workflow:
    User Question
        ↓
    Check Redis Cache
        ↓
    Cache Hit?
        ↓
    Yes → Return Cached Response
        ↓
    No
        ↓
    Retrieve Relevant Chunks
        ↓
    Build Context
        ↓
    Augment Prompt
        ↓
    Generate AI Answer
        ↓
    Cache Response
        ↓
    Return Response
    """

    def __init__(
        self,
        retrieval_service: RetrievalService,
    ):
        self.retrieval_service = retrieval_service

    def generate_answer(
        self,
        question: str,
    ) -> RAGResponse:
        """
        Generate a context-aware answer using retrieved documents.
        """
        try:

            # -----------------------------
            # Check Redis Cache
            # -----------------------------
            cached_response = cache_service.get(question)

            if cached_response:
                logger.info(
                    "Cache hit. Returning response from Redis."
                )

                cached_data = json.loads(cached_response)

                return RAGResponse(**cached_data)

            logger.info(
                "Cache miss. Generating new response."
            )

            # -----------------------------
            # Retrieve Relevant Documents
            # -----------------------------
            results = self.retrieval_service.retrieve(question)

            documents = results["documents"]
            metadatas = results["metadatas"]

            if not documents:
                logger.warning(
                    "No relevant documents found for the given question."
                )

                return RAGResponse(
                    answer="No relevant information was found in the uploaded documents.",
                    sources=[],
                )

            # -----------------------------
            # Build Context
            # -----------------------------
            context = "\n\n".join(documents)

            prompt = RAG_PROMPT.format(
                context=context,
                question=question,
            )

            # -----------------------------
            # Generate AI Response
            # -----------------------------
            answer = generate_response(prompt)

            # -----------------------------
            # Collect Sources
            # -----------------------------
            sources = []

            for metadata in metadatas:
                filename = metadata.get("filename")

                if filename and filename not in sources:
                    sources.append(filename)

            response = RAGResponse(
                answer=answer,
                sources=sources,
            )

            # -----------------------------
            # Cache Response
            # -----------------------------
            cache_service.set(
                question=question,
                value=json.dumps(
                    response.model_dump(),
                    ensure_ascii=False,
                ),
            )

            logger.info(
                "RAG response cached successfully."
            )

            return response

        except Exception:
            logger.exception(
                "Failed to generate RAG response."
            )
            raise
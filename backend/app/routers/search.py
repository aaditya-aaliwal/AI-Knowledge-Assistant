from fastapi import APIRouter, Depends

from app.dependencies import get_retrieval_service
from app.schemas.search_schema import SearchRequest
from app.services.retrieval_service import RetrievalService


router = APIRouter(
    prefix="/search",
    tags=["Search"],
)


@router.post("")
def search(
    request: SearchRequest,
    retrieval_service: RetrievalService = Depends(
        get_retrieval_service
    ),
):
    results = retrieval_service.retrieve(
        request.question
    )

    return results
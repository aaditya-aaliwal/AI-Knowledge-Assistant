import hashlib

from app.cache.redis_client import redis_client
from app.config import settings


class CacheService:

    def _generate_key(
        self,
        question: str
    ) -> str:

        question_hash = hashlib.sha256(
            question.encode("utf-8")
        ).hexdigest()

        return f"rag:{question_hash}"

    def get(
        self,
        question: str
    ) -> str | None:

        key = self._generate_key(question)

        return redis_client.get(key)

    def set(
        self,
        question: str,
        value: str,
        ttl: int | None = None
    ) -> None:

        key = self._generate_key(question)

        redis_client.set(
            name=key,
            value=value,
            ex=ttl or settings.REDIS_CACHE_TTL
        )

    def delete(
        self,
        question: str
    ) -> None:

        key = self._generate_key(question)

        redis_client.delete(key)


cache_service = CacheService()
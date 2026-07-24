from pydantic_settings import BaseSettings, SettingsConfigDict



class Settings(BaseSettings):
    APP_NAME: str
    APP_VERSION: str
    DEBUG: bool
    SECRET_KEY: str
    ALGORITHM: str
    ACCESS_TOKEN_EXPIRE_MINUTES: int
    REFRESH_TOKEN_EXPIRE_DAYS: int
    GEMINI_API_KEY: str
    GEMINI_MODEL: str
    GEMINI_TEMPERATURE: float = 0.2
    GEMINI_EMBEDDING_MODEL: str

    CHUNK_SIZE: int = 1000
    CHUNK_OVERLAP: int = 200

    CHROMA_DB_PATH: str 
    CHROMA_COLLECTION_NAME: str 


    # PostgreSQL Configuration
    DB_HOST: str
    DB_PORT: int
    DB_NAME: str
    DB_USER: str
    DB_PASSWORD: str


    # Redis Configuration
    REDIS_HOST: str
    REDIS_PORT: int
    REDIS_DB: int
    REDIS_PASSWORD: str = ""
    REDIS_DECODE_RESPONSES: bool = True
    REDIS_CACHE_TTL: int


    # RabbitMQ Configuration
    RABBITMQ_HOST: str
    RABBITMQ_PORT: int
    RABBITMQ_USERNAME: str
    RABBITMQ_PASSWORD: str
    RABBITMQ_QUEUE: str

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8"
    )


settings = Settings()
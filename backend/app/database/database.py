from sqlalchemy import create_engine, inspect, text
from sqlalchemy.orm import sessionmaker, declarative_base
from app.config import settings

DATABASE_URL = (
    f"postgresql://{settings.DB_USER}:"
    f"{settings.DB_PASSWORD}@"
    f"{settings.DB_HOST}:"
    f"{settings.DB_PORT}/"
    f"{settings.DB_NAME}"
)

engine = create_engine(DATABASE_URL)

SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)

Base = declarative_base()


def ensure_document_columns(db_engine) -> None:
    """Apply the small additive document metadata migration for existing installs."""
    inspector = inspect(db_engine)
    if "documents" not in inspector.get_table_names():
        return

    existing_columns = {column["name"] for column in inspector.get_columns("documents")}
    additions = {
        "filepath": "VARCHAR(500)",
        "uploaded_by": "INTEGER",
        "status": "VARCHAR(20) NOT NULL DEFAULT 'UPLOADING'",
    }
    with db_engine.begin() as connection:
        for name, definition in additions.items():
            if name not in existing_columns:
                connection.execute(text(f"ALTER TABLE documents ADD COLUMN {name} {definition}"))
        connection.execute(text("ALTER TABLE documents ALTER COLUMN filename TYPE VARCHAR(255)"))

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

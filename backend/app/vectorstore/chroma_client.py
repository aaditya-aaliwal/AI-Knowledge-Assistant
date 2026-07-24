import chromadb

from app.config import settings

chroma_client = chromadb.PersistentClient(
    path=settings.CHROMA_DB_PATH
)

collection = chroma_client.get_or_create_collection(
    name=settings.CHROMA_COLLECTION_NAME
)

print(f"Collection Name : {collection.name}")
print(f"Total Vectors   : {collection.count()}")
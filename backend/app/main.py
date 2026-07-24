from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

from fastapi import Depends
from app.dependencies import get_app_name

from app.utils import print_app_info
from app.cache.redis_client import redis_client
from app.logger import logger


from app.routers import users,chats,documents,auth,ai,ai_chat,search,rag

from app.database.database import Base, engine, ensure_document_columns

from app.config import settings


Base.metadata.create_all(bind=engine)
ensure_document_columns(engine)

app = FastAPI()

# The browser client is served separately by Vite in development.  Keep this
# explicit so authenticated requests can be made without opening the API to
# arbitrary origins.
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://127.0.0.1:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
logger.info("Application Started")

print_app_info()


app.include_router(users.router)

app.include_router(chats.router)

app.include_router(documents.router)

app.include_router(auth.router)

app.include_router(ai.router)

app.include_router(ai_chat.router)

app.include_router(search.router)

app.include_router(rag.router)






@app.on_event("startup")
def startup_event():
    try:
        redis_client.ping()
        logger.info("Redis connected successfully.")
    except Exception as e:
        logger.error(f"Redis connection failed: {e}")



@app.get("/dependency")
def dependency_demo(
    app_name = Depends(get_app_name)
):
    return {
        "app_name": app_name
    }

@app.get("/")
def home():
    return JSONResponse(
        status_code=200,
        content={
            "message": "Welcome to AI Knowledge Assistant Backend"
        }
    )

@app.get("/health")
def health():
    return JSONResponse(
        status_code=200,
        content={
            "status": "healthy"
        }
    )

@app.get("/version")
def version():
    return JSONResponse(
        status_code=200,
        content={
            "version": settings.APP_VERSION
        }
    )


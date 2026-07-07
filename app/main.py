from fastapi import FastAPI
from fastapi.responses import JSONResponse

from fastapi import Depends
from app.dependencies import get_app_name

from app.utils import print_app_info
from app.logger import log_info
from app.config import APP_VERSION


from app.routers import users,chats,documents

from app.database.database import Base, engine
from app.models import User,Chat,Document

Base.metadata.create_all(bind=engine)





app = FastAPI()
log_info("Application Started")

print_app_info()


app.include_router(users.router)

app.include_router(chats.router)

app.include_router(documents.router)


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
            "version": APP_VERSION
        }
    )



@app.get("/search")
def search_user(name: str):
    return {
        "search": name
    }

@app.get("/products")
def get_products(limit: int = 10):
    return {
        "limit": limit
    }

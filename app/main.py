from fastapi import FastAPI
from fastapi.responses import JSONResponse

from app.utils import print_app_info
from app.logger import log_info
from app.config import APP_VERSION


app = FastAPI()
log_info("Application Started")

print_app_info()

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
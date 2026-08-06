from fastapi import FastAPI
from app.core.config import settings
from app.core.logger import logger
from app.api.v1.upload import router as upload_router


app = FastAPI(
    title=settings.app_name,
    description=settings.app_description,
    version=settings.app_version
)

logger.info("Compliance Surveillance application started")


@app.get("/")
def root():
    logger.info("Root endpoint called")
    return {
        "application": settings.app_name,
        "version": settings.app_version,
        "description": settings.app_description,
        "status": "running"
    }


@app.get("/health")
def health():
    logger.info("Health endpoint called")
    return {
        "status": "healthy"
    }


app.include_router(upload_router)

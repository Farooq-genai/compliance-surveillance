from fastapi import FastAPI
from app.core.config import settings
from app.core.logger import logger
from app.api.v1.upload import router as upload_router
from app.api.v1.compliance import router as compliance_router
from app.api.v1.risk_matrix import router as risk_matrix_router
from fastapi.responses import HTMLResponse
from pathlib import Path


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

@app.get("/dashboard", response_class=HTMLResponse)

def dashboard():

    file = Path(
        "app/templates/compliance_dashboard.html"
    )

    return file.read_text(
        encoding="utf-8"
    )


app.include_router(
    risk_matrix_router,
    prefix="/api"
)

app.include_router(upload_router)
app.include_router(compliance_router, prefix="/api/v1")

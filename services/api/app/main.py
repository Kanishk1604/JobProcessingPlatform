from fastapi import FastAPI

from app.api.routes.health import router as health_router
from app.api.routes.documents import router as documents_router
from app.api.routes.jobs import router as jobs_router
from app.api.routes.job_queries import router as job_queries_router 
from app.core.config import get_settings

settings = get_settings()

app = FastAPI(
    title=settings.app_name,
    version="0.1.0"
)

app.include_router(health_router, prefix="/v1")
app.include_router(documents_router, prefix="/v1")
app.include_router(jobs_router, prefix="/v1")
app.include_router(job_queries_router, prefix="/v1")

@app.get("/")
def root() -> dict[str,str]:
    return {
        "services" : settings.app_name,
        "environment": settings.app_env,
        "status" : "running",
    }
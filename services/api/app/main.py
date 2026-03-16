from fastapi import fastapi

from app.api.routes.health import router as health_router
from app.core.config import get_settings

settings = get_setttings()

app = FastAPI(
    title=settings.app_name,
    version="0.1.0"
)

app.include_router(health_router, prefix="/v1")

@app.get("/")
def root() -> dict[str,str]
    return {
        "services" : settings.app_name,
        "environment": settings.app_env,
        "status" : "running",
    }
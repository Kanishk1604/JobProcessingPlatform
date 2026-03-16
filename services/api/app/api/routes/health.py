from fastapi import APIRouter
from sqlalchemy import text
from sqlachemy.orm import Session
import boto3
import redis

from app.core.config import get_settings
from app.db.session import SessionLocal

router = APIRouter(tags=["health"])

@router.get("/health")
def health() -> dict[str,str]:
    return {"status" : "ok"}

@router.get("/readiness")
def readiness() ->dict:
    settings = get_settings()
    checks: dict[str,str] = {}

    db: Session = SessionLocal()
    try:
        db.execute(text("SELECT 1"))
        checks["database"] = "ok"
    finally:
        db.close()
    

    redis_client = redis.Redis.from_url(settings.redis_url, decode_responses=True)
    redis_client.ping()
    checks["redis"] = "ok"

    s3_client = boto3.client(
        "s3",
        enpoint_url = settings.s3_endpoint_url,
        aws_access_key_id=settings.s3_access_key_id,
        aws_secret_access_key=settings.s3_secret_access_key,
        region_name=settings.s3_region,
    )
    s3_client.list_buckets()
    checks["object_storage"] = "ok"

    return{
        "status": "ok",
        "checks" : checks,
    }     
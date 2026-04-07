from datetime import datetime
from uuid import UUID 

from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.models.job import Job
from app.models.job_event import JobEvent

router = APIRouter(tags = ["jobs"])

class JobDetailResponse(BaseModel):
    id: UUID 
    docuemnt_id: UUID 
    job_type: str
    status: str
    priority: int 
    attempt_count: int
    correlation_id: str
    error_code: str | None
    error_message: str | None
    result_storage_key: str | None
    queued_at:  datetime | None
    started_at: datetime | None
    completed_at: datetime | None
    created_at: datetime
    updated_at: datetime

    model_config = {"from_attributes": True}

class JobEventResponse(BaseModel):
    id: UUID
    job_id: UUID
    event_type: str
    payload_json: dict
    created_at: datetime

    model_config = {"from_attributes": True}

class JobEventListResponse(BaseModel):
    items: list[JobEventResponse]


@router.get("/jobs/{job_id}", response_model= JobDetailResponse)
def get_job(
    job_id: UUID, 
    db: Session = Depends(get_db),
)-> JobDetailResponse:

    job = db.get(Job, job_id)

    if job is None: 
        raise HTTPException(
            status_code = status.HTTP_404_NOT_FOUND,
            deatil="Job not found",
        )
    
    return job

@router.get("/jobs/{job_id}/events", response_model = JobEventListResponse)
def get_job_events(
    job_id: UUID,
    db: Session = Depends(get_db),
)-> JobEventListResponse:

    job = db.get(Job, job_id)

    if job is None:
        raise HTTPException(
            status_code = status.HTTP_404_NOT_FOUND,
            deatil="Job not found",
        )
    
    stmt = (
        select(JobEvent) 
        .where(JobEvent.job_id== job_id)
        .order_by(JobEvent.created_at.asc())
    )

    events = db.execute(stmt).scalars().all()

    return JobEventListResponse(items = events)
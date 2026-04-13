from datetime import datetime
from uuid import UUID 

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.responses import PlainTextResponse
from pydantic import BaseModel
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.models.job import Job
from app.models.document import Document
from app.models.job_event import JobEvent
from app.services.storage_service import StorageService

router = APIRouter(tags = ["jobs"])

class JobDetailResponse(BaseModel):
    id: UUID 
    document_id: UUID 
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
            detail="Job not found",
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
            detail="Job not found",
        )
    
    stmt = (
        select(JobEvent) 
        .where(JobEvent.job_id== job_id)
        .order_by(JobEvent.created_at.asc())
    )

    events = db.execute(stmt).scalars().all()

    return JobEventListResponse(items = events)

    #get/v1/jobs/id/result
# check if job exists
# ensure that the job has succeeded 
# read result file from minio -> same way we read when download from minio
# return extracted text or file contents -> decode to utf-8 
# response_class= PlainTextResponse,
@router.get("/jobs/{job_id}/result", status_code=status.HTTP_200_OK)
def get_resulted_document(
    job_id : UUID,
    db: Session = Depends(get_db), 
):

    job = db.get(Job, job_id)

    #Validating the job_id
    if job is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail= "Job not found",
        )
    
    if job.status != "SUCCEEDED":
        raise ValueError (f"The job status is not Succeeded yet")

    if not job.result_storage_key:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Result not available",
        )
    
    #Downloading the file from minIO
    storage_service = StorageService()
    file_bytes = storage_service.download_bytes(job.result_storage_key)
    extracted_txt = file_bytes.decode("utf-8")

    document = db.get(Document, job.document_id)

    if document is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Document not found",
        )

    return {
        "document_id": str(document.id),
        "job_id": str(job_id),
        "mime_type": document.mime_type,
        "original_filename": document.original_filename,
        "extracted_txt": extracted_txt,
        "character_count": len(extracted_txt),
        "word_count": len(extracted_txt.split()),
    }
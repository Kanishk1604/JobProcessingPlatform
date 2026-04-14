import uuid

from fastapi import APIRouter, Depends, status, HTTPException, File
from sqlalchemy.orm import Session

from app.core.celery_app import celery_app
from app.core.task_names import PROCESS_DOCUMENT_TASK 
from app.db.session import get_db
from app.models.job import Job
from app.models.document import Document
from app.models.job_event import JobEvent
from app.services.storage_service import StorageService
from app.schemas.job import JobCreateRequest, JobResponse

from app.observability.metrics import jobs_created_total

router = APIRouter(tags=["jobs"])

@router.post("/jobs",response_model= JobResponse, status_code=status.HTTP_201_CREATED)
def creat_job(
    payload: JobCreateRequest,
    db: Session = Depends(get_db),
) -> JobResponse:
    document = db.get(Document, payload.document_id)

    if document is None:
        raise HTTPException(
            status_code = status.HTTP_404_NOT_FOUND,
            detail = "Document not found"
        )
    
    job_id = uuid.uuid4()
    correlation_id= uuid.uuid4()

    job = Job(
        id=job_id,
        document_id=payload.document_id,
        job_type= payload.job_type,
        status="QUEUED",
        priority=5,
        attempt_count=0,
        max_attempts=3,
        correlation_id=correlation_id,
    )

    db.add(job)

    job_created_event = JobEvent(
        job_id= job_id,
        event_type= "JOB_CREATED",
        payload_json={
            "status": "QUEUED",
            "job_type": payload.job_type,
            "document_id": str(payload.document_id)
        }
    )

    db.add(job_created_event)

    job_queued_event = JobEvent(
        job_id=job_id,
        event_type="JOB_QUEUED",
        payload_json={
            "status": "QUEUED",
        },
    )
    db.add(job_queued_event)

    db.commit()
    db.refresh(job)

    celery_app.send_task(
        PROCESS_DOCUMENT_TASK,
        kwargs={
            "job_id": str(job.id),
        },
    )

    jobs_created_total.inc()    #observability

    return job





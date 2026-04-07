#first worker task

from datetime import datetime
from uuid import UUID 

from app.celery_app import celery_app
from app.db.session import SessionLocal
from app.models.job import job
from app.models.job_event import JobEvent

@celery_app.task(name="worker.tasks.process_document")
def process_document(job_id: str) -> dict:
    db = SessionLocal()

    try:
        job = db.get(Job, UUID(job_id))
        if job is None:
            return{"status": "missing_job", "job_id": job_id}

        job.status = "RUNNING"
        job.started_at = datetime.utcnow()
        job.attempt_count += 1

        db.add(
            JobEvent(
                job_id=job_id,
                event_type="JOB_STARTED",
                payload_json={"status": "RUNNING"},
            )
        )

        db.commit()

        
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

        # temp fake processing
        job.status = "SUCCEEDED"
        job.completed_at = datetime.utcnow()

        db.add(
            JobEvent(
                job_id=job_id,
                event_type="JOB_COMPLETED",
                payload_json={"status": "SUCCEEDED"},
            )
        )
        
        db.commit()

        return {"status": "ok", "job_id": job_id}
    except Exception as exc:
        db.rollback()

        job = db.get(Job, UUID(job_id))

        if job is not None:
            job.status = "FAILED_TERMINAL"
            job.completed_at = datetime.utcnow()
            job.error_code = "PROCESSING_ERROR"
            job.error_message = str(exc)

            db.add(
                JobEvent(
                    job_id=job_id,
                    event_type="JOB_FAILED",
                    payload_json={
                        "status": "FAILED_TERMINAL",
                        "error": str(exc),
                    },
                )
            )
            db.commit()
            raise
    finally:
        db.close()
#first worker task

from datetime import datetime, UTC
from uuid import UUID 

from app.celery_app import celery_app
from app.db.session import SessionLocal
from app.models.document import Document
from app.models.job import Job
from app.models.job_event import JobEvent
from app.services.storage_service import StorageService

@celery_app.task(name="worker.tasks.process_document")
def process_document(job_id: str) -> dict:
    db = SessionLocal()
    storage_service = StorageService()

    try:
        job = db.get(Job, UUID(job_id))
        if job is None:
            return{"status": "missing_job", "job_id": job_id}

        document = db.get(Document, job.document_id)

        if document is None:
            job.status = "FAILED_TERMINAL"
            job.completed_at = datetime.now(UTC)
            job.error_code = "Document_not_found"
            job.error_message = "Document record not found"
            
            db.add(
                JobEvent(
                    job_id=job_id,
                    event_type="JOB_FAILED",
                    payload_json={
                        "status": "FAILED_TERMINAL",
                        "error": "Document not found",
                    },
                )
            )
            db.commit()
            return {"status": "document_missing", "job_id": job_id}

        job.status = "RUNNING"
        job.started_at = datetime.now(UTC)
        job.attempt_count += 1

        db.add(
            JobEvent(
                job_id=job_id,
                event_type="JOB_STARTED",
                payload_json={"status": "RUNNING"},
            )
        )

        db.commit()

        if document.mime_type != "text/plain":
            raise ValueError (f"Unsupported mime type for v1 processor: {document.mime_type}")
        
        file_bytes = storage_service.download_bytes(document.storage_key)
        extracted_txt = file_bytes.decode("utf-8")

        result_key = f"results/{job_id}/extracted.txt"

        storage_service.upload_bytes(
            data= extracted_txt.encode("utf-8"),
            key=result_key,
            content_type="text/plain",
        )

        job.result_storage_key = result_key
        job.status = "SUCCEEDED"
        job.completed_at = datetime.now(UTC)

        db.add(
            JobEvent(
                job_id=job_id,
                event_type="JOB_COMPLETED",
                payload_json={"status": "SUCCEEDED",
                              "result_storage_key": result_key,
                        },
            )
        )
        
        db.commit()

        return {"status": "ok", "job_id": job_id}
    except Exception as exc:
        db.rollback()

        job = db.get(Job, UUID(job_id))

        if job is not None:
            job.status = "FAILED_TERMINAL"
            job.completed_at = datetime.now(UTC)
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
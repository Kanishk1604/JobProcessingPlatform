from sqlalchemy import func, select
from sqlalchemy.orm import Session

from app.models.job import Job
from app.observability.metrics import (
    jobs_failed_retryable_current,
    jobs_failed_terminal_current,
    jobs_queued_current,
    jobs_running_current,
    jobs_succeeded_current,
)

def _count_job_by_status(db: Session, status_value: str) -> int:
    stmt = select(func.count()).select_from(Job).where(Job.status == status_value)
    return db.execute(stmt).scalar_one()

def refresh_job_state_gauges(db:Session) -> None:
    jobs_failed_retryable_current.set(_count_job_by_status(db, "FAILED_RETRYABLE"))
    jobs_failed_terminal_current.set(_count_job_by_status(db, "FAILED_TERMINAL"))
    jobs_queued_current.set(_count_job_by_status(db, "QUEUED"))
    jobs_running_current.set(_count_job_by_status(db, "RUNNING"))
    jobs_succeeded_current.set(_count_job_by_status(db, "SUCCEEDED"))
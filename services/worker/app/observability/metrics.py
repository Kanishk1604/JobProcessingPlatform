#prometheus_client -> exposes data
from prometheus_client import Counter, Histogram

jobs_started_total = Counter(
    "jobs_started_total",
    "Total number of jobs started by worker",
)

jobs_succeeded_total = Counter(
    "jobs_succeeded_total",
    "Total number of jobs succeeded by worker",
)

jobs_failed_terminal_total = Counter(
    "jobs_failed_terminal_total",
    "Total number of jobs that failed terminally",
)

jobs_failed_retryable_total = Counter(
    "jobs_failed_retryable_total",
    "Total number of jobs that failed retryably",
)

job_processing_seconds = Histogram(
    "job_processing_seconds",
    "Time spent processing jobs in seconds",
)
from prometheus_client import Counter, Gauge

documents_uploaded_total = Counter(
    "documents_uploaded_total",
    "Total number of uploaded documents",
)

jobs_created_total = Counter(
    "jobs_created_total",
    "Total number of jobs created",
)

jobs_queued_current = Gauge(
    "jobs_queued_current",
    "Current number of queued jobs",
)

jobs_running_current = Gauge(
    "jobs_running_current",
    "Current number of runnning jobs",
)

jobs_succeeded_current = Gauge(
    "jobs_succeeded_current",
    "Current number of succeeded jobs",
)

jobs_failed_terminal_current = Gauge(
    "jobs_failed_terminal_current",
    "Current number of terminally failed jobs",
)

jobs_failed_retryable_current = Gauge(
    "jobs_failed_retryable_current",
    "Current number of retryably failed jobs",
)

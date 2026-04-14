from prometheus_client import Counter

documents_uploaded_total = Counter(
    "documents_uploaded_total",
    "Total number of uploaded documents",
)

jobs_created_total = Counter(
    "jobs_created_total",
    "Total number of jobs created",
)
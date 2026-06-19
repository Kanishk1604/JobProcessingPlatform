Document Processing Platform

A production-style document processing platform built with FastAPI, PostgreSQL, Redis, Celery, MinIO, Prometheus, and Grafana.

The platform supports document ingestion, asynchronous processing, event tracking, result retrieval, and operational monitoring.

⸻

Features

* Upload documents through REST APIs
* Store document metadata in PostgreSQL
* Store files in MinIO (S3-compatible object storage)
* Create asynchronous processing jobs
* Process jobs using Celery workers
* Track job lifecycle through event history
* Retrieve processed document results
* Monitor system health with Prometheus and Grafana
* Expose operational metrics and dashboards

⸻

Architecture

                    ┌─────────────┐
                    │   Client    │
                    └──────┬──────┘
                           │
                           ▼
                    ┌─────────────┐
                    │  FastAPI    │
                    │    API      │
                    └──────┬──────┘
                           │
         ┌─────────────────┼─────────────────┐
         ▼                 ▼                 ▼
 ┌────────────┐   ┌────────────┐   ┌────────────┐
 │ PostgreSQL │   │   Redis    │   │   MinIO    │
 │ Metadata   │   │ Job Queue  │   │ File Store │
 └────────────┘   └──────┬─────┘   └────────────┘
                          │
                          ▼
                   ┌─────────────┐
                   │ Celery      │
                   │ Worker      │
                   └──────┬──────┘
                          │
                          ▼
                   ┌─────────────┐
                   │ Result      │
                   │ Storage     │
                   └─────────────┘
Prometheus ─────► Metrics Collection
Grafana    ─────► Dashboard Visualization

⸻

Technology Stack

Component	       Technology
API	              FastAPI
Database	        PostgreSQL
ORM	              SQLAlchemy
Migrations	      Alembic
Queue	            Redis
Workers	          Celery
Object Storage	  MinIO
Monitoring	      Prometheus
Dashboards	      Grafana
Containerization	Docker Compose

⸻

Job Lifecycle

RECEIVED
    │
    ▼
QUEUED
    │
    ▼
RUNNING
    │
    ├────────────► SUCCEEDED
    │
    ├────────────► FAILED_TERMINAL
    │
    └────────────► FAILED_RETRYABLE

Each transition is recorded in the job_events table for observability and auditing.

⸻

Data Model

Documents

Stores uploaded document metadata.

Field	              Description
id	                Document identifier
original_filename	  Original uploaded filename
mime_type	          File content type
size_bytes	        File size
storage_bucket	    MinIO bucket
storage_key	Object  storage key

Jobs

Represents asynchronous processing requests.

Field	              Description
id	                Job identifier
document_id	        Associated document
status	            Current job state
job_type	          Processing type
attempt_count	      Retry count
result_storage_key	Result location

Job Events

Stores immutable job state transitions.

Example:

{
  "event_type": "JOB_STARTED",
  "status": "RUNNING"
}
{
  "event_type": "JOB_COMPLETED",
  "status": "SUCCEEDED"
}

⸻

API Endpoints

Upload Document

POST /v1/documents/upload

Example:

curl -X POST http://localhost:8000/v1/documents/upload \
  -F "file=@sample.txt;type=text/plain"

⸻

Create Job

POST /v1/jobs

Request:

{
  "document_id": "<document_id>",
  "job_type": "extract_text"
}

⸻

Get Job

GET /v1/jobs/{job_id}

Returns current job status and metadata.

⸻

Get Job Events

GET /v1/jobs/{job_id}/events

Returns the complete job lifecycle history.

⸻

Get Job Result

GET /v1/jobs/{job_id}/result

Returns extracted document content and metadata.

⸻

Local Development

Start All Services

docker compose -f infra/docker/docker-compose.yml up --build

Stop Services

docker compose -f infra/docker/docker-compose.yml down

Verify Health

curl http://localhost:8000/v1/health

Expected response:

{
  "service": "doc-api",
  "environment": "local",
  "status": "running"
}

⸻

Observability

API Metrics

curl http://localhost:8000/metrics

Example metrics:

documents_uploaded_total
jobs_created_total
jobs_queued_current
jobs_running_current
jobs_succeeded_current
jobs_failed_terminal_current
jobs_failed_retryable_current

Worker Metrics

curl http://localhost:9002/metrics

Example metrics:

jobs_started_total
jobs_succeeded_total
jobs_failed_terminal_total
jobs_failed_retryable_total
job_processing_seconds

Prometheus

http://localhost:9090

Grafana

http://localhost:3000

Default credentials:

Username: admin
Password: admin

⸻

Dashboard Metrics

Throughput

* Documents Uploaded Total
* Jobs Created Total
* Jobs Started Total

Current Job State

* Queued Jobs
* Running Jobs
* Succeeded Jobs
* Failed Terminal Jobs
* Failed Retryable Jobs

Reliability & Performance

* Jobs Succeeded Total
* Jobs Failed Terminal Total
* Jobs Failed Retryable Total
* Average Processing Time

⸻

Current Processing Support

Supported

* text/plain

Planned

* application/pdf
* OCR-based document extraction
* Multi-document batch processing

⸻

Future Enhancements

* PDF text extraction
* Retry backoff policies
* Dead letter queue support
* Kubernetes deployment
* AWS S3 integration
* OpenTelemetry tracing
* Authentication and authorization
* Multi-tenant document processing
* Event-driven notification system

⸻

Learning Outcomes

This project demonstrates:

* REST API design
* Asynchronous job processing
* Event-driven architecture
* Object storage integration
* Database migrations
* Observability and monitoring
* Containerized deployments
* Production-oriented backend engineering
* Distributed systems fundamentals
* Operational dashboarding and metrics collection

⸻

License

MIT License

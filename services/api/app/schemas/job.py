from datetime import datetime
from uuid import UUID 

from pydantic import BaseModel, Field

class JobCreateRequest(BaseModel):
    document_id: UUID 
    job_type: str = Field(min_length=1, max_length= 100)

class JobResponse(BaseModel):
    id: UUID 
    document_id: UUID
    job_type: str
    status: str
    priority: int
    attempt_count: int
    max_attempts: int
    correlation_id: str
    created_at: datetime

    model_config = {"from_attributes": True}
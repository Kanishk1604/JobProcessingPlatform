from datetime import datetime
from uuid import UUID 

from pydantic import BaseModel, Field

class DocumentCreateRequest(BaseModel):
    original_filename: str = Field(min_length=1, max_length=512)
    mime_type: str = Field(min_length=1, max_length=255)
    size_bytes: int = Field(gt=0)

class DocumentResponse(BaseModel):
    id: UUID 
    original_filename: str
    mime_type: str
    size_bytes: int
    storage_bucket: str
    storage_key: str
    created_at: datetime

    model_config = {"from_attributes": True}
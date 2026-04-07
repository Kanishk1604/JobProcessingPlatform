import uuid 

from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from app.core.config import get_settings
from app.db.session import get_db
from app.models.document import Document
from app.schemas.document import DocumentCreateRequest, DocumentResponse

router = APIRouter(tags= ["Documents"])

@router.post("/documents", response_model = DocumentResponse, status_code= status.HTTP_201_CREATED)
def create_document(
    payload: DocumentCreateRequest,
    db: Session = Depends(get_db),
) -> DocumentResponse:
    settings = get_settings()

    document_id = uuid.uuid4()
    storage_key = f"raw/{document_id}/{payload.original_filename}"

    document = Document(
        id = document_id,
        original_filename = payload.original_filename,
        mime_type = payload.mime_type,
        size_bytes = payload.size_bytes,
        storage_bucket = settings.s3_bucket_name,
        storage_key = storage_key,
    )

    db.add(document)
    db.commit()
    db.refresh(document)

    return document
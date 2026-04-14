import uuid 
from pathlib import Path
from fastapi import APIRouter, Depends, status, HTTPException, UploadFile, File
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.models.document import Document
from app.schemas.document import DocumentCreateRequest, DocumentResponse
from app.services.storage_service import StorageService

from app.observability.metrics import documents_uploaded_total

router = APIRouter(tags= ["Documents"])

ALLOWED_CONTENT_TYPES = {
    "text/plain",           #.txt
    "application/pdf",
}

MAX_FILE_SIZE_BYTES =  10 * 1024 * 1024 


@router.post("/documents/upload", response_model = DocumentResponse, status_code= status.HTTP_201_CREATED)
async def create_document(
    file: UploadFile = File(...),
    db: Session = Depends(get_db),
) -> DocumentResponse:

    if not file.filename:
        raise HTTPException(
            status_code = status.HTTP_400_BAD_REQUEST,
            detail= "Filename is required"
        )
    
    content_type = file.content_type or "application/octet-stream"

    if content_type not in ALLOWED_CONTENT_TYPES:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Unsupported content type: {content_type}",
        )

    contents = await file.read()

    if not contents:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="File cannot be empty",
        )

    if len(contents) > MAX_FILE_SIZE_BYTES:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="File exceeds size limit",
        )

    document_id = uuid.uuid4()
    safe_filename= Path(file.filename).name
    storage_key = f"raw/{document_id}/{safe_filename}"

    storage_service = StorageService()
    storage_service.upload_bytes(
        data=contents,
        key = storage_key,
        content_type = content_type,
    )

    document = Document(
        id = document_id,
        original_filename = safe_filename,
        mime_type = content_type,
        size_bytes = len(contents),
        storage_bucket = storage_service.bucket_name,
        storage_key = storage_key,
    )

    db.add(document)
    db.commit()
    db.refresh(document)

    documents_uploaded_total.inc()  #observability

    return document
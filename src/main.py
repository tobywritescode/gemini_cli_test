import uuid
from decimal import Decimal
from contextlib import asynccontextmanager
from fastapi import FastAPI, Depends, HTTPException, UploadFile, File, Form, BackgroundTasks, status
from sqlalchemy.orm import Session

from src.database import engine, Base
from src.models import InvoiceMetadata, UploadStatus
from src.schemas import UploadResponse
from src.dependencies import get_db, get_current_vendor_id
from src.tasks import upload_to_s3

# SEC-05 Remediation: Use lifespan handler instead of @app.on_event("startup")
@asynccontextmanager
async def lifespan(app: FastAPI):
    # SEC-02 Remediation: Ensure tables are created at startup
    Base.metadata.create_all(bind=engine)
    yield
    # Cleanup logic (if any) could go here

app = FastAPI(title="Invoice Upload Service", lifespan=lifespan)

@app.post("/upload", response_model=UploadResponse, status_code=status.HTTP_202_ACCEPTED)
async def upload_invoice(
    background_tasks: BackgroundTasks,
    vendor_id: str = Form(...),
    invoice_amount: Decimal = Form(...),
    file: UploadFile = File(...),
    current_vendor: str = Depends(get_current_vendor_id),
    db: Session = Depends(get_db)
):
    # Security Check: Ownership (RBAC)
    if vendor_id != current_vendor:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Vendor ID mismatch")

    # Validation: File Size (5MB)
    MAX_FILE_SIZE = 5 * 1024 * 1024
    file_content = await file.read()
    if len(file_content) > MAX_FILE_SIZE:
        raise HTTPException(status_code=status.HTTP_413_REQUEST_ENTITY_TOO_LARGE, detail="File too large")

    # Validation: Magic Bytes
    if not file_content.startswith(b"%PDF-"):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid File Type: Not a PDF")

    # Persistence
    track_id = uuid.uuid4()
    new_invoice = InvoiceMetadata(
        id=track_id,
        vendor_id=vendor_id,
        invoice_amount=invoice_amount,
        status=UploadStatus.PENDING
    )
    db.add(new_invoice)
    db.commit()

    # Async Offloading
    background_tasks.add_task(upload_to_s3, track_id, file_content)

    return UploadResponse(
        track_id=track_id,
        status=UploadStatus.PENDING,
        message="Invoice upload initiated."
    )

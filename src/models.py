import uuid
from datetime import datetime
from enum import Enum as PyEnum
from sqlalchemy import Column, String, Numeric, DateTime, Enum, UUID as SQLUUID
from src.database import Base

class UploadStatus(str, PyEnum):
    PENDING = "PENDING"
    COMPLETED = "COMPLETED"
    FAILED = "FAILED"

class InvoiceMetadata(Base):
    __tablename__ = "invoice_metadata"
    id = Column(SQLUUID, primary_key=True, default=uuid.uuid4)
    vendor_id = Column(String, nullable=False, index=True)
    invoice_amount = Column(Numeric(precision=12, scale=2), nullable=False)
    file_path = Column(String, nullable=True)
    status = Column(Enum(UploadStatus), default=UploadStatus.PENDING, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)

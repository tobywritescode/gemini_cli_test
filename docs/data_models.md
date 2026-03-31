# Data Models: Invoice Upload Microservice

## PostgreSQL Schema (SQLAlchemy)

```python
from uuid import UUID, uuid4
from datetime import datetime
from enum import Enum as PyEnum
from sqlalchemy import Column, String, Numeric, DateTime, Enum, UUID as SQLUUID
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class UploadStatus(str, PyEnum):
    PENDING = "PENDING"
    COMPLETED = "COMPLETED"
    FAILED = "FAILED"

class InvoiceMetadata(Base):
    __tablename__ = "invoice_metadata"

    id = Column(SQLUUID, primary_key=True, default=uuid4)
    vendor_id = Column(String, nullable=False, index=True)
    invoice_amount = Column(Numeric(precision=12, scale=2), nullable=False)
    file_path = Column(String, nullable=True)  # S3 Key/Path
    status = Column(Enum(UploadStatus), default=UploadStatus.PENDING, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
```

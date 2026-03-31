import uuid
from decimal import Decimal
from pydantic import BaseModel
from src.models import UploadStatus

class UploadResponse(BaseModel):
    track_id: uuid.UUID
    status: UploadStatus
    message: str

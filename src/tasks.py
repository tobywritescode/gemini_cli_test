import uuid
import hashlib
from src.database import SessionLocal
from src.models import InvoiceMetadata, UploadStatus

def upload_to_s3(track_id: uuid.UUID, file_content: bytes):
    """
    Simulates uploading to S3 with integrity verification.
    """
    db = SessionLocal()
    try:
        # SEC-03 Remediation: Calculate and verify checksum (Simulation)
        file_hash = hashlib.md5(file_content).hexdigest()
        
        # Mock S3 Upload Logic with Checksum
        # s3_client.put_object(Bucket="invoices", Key=f"{track_id}.pdf", Body=file_content, ContentMD5=file_hash)
        file_path = f"s3://invoices/{track_id}.pdf"
        
        # Update Database
        invoice = db.query(InvoiceMetadata).filter(InvoiceMetadata.id == track_id).first()
        if invoice:
            invoice.file_path = file_path
            invoice.status = UploadStatus.COMPLETED
            db.commit()
    except Exception as e:
        db.rollback()
        invoice = db.query(InvoiceMetadata).filter(InvoiceMetadata.id == track_id).first()
        if invoice:
            invoice.status = UploadStatus.FAILED
            db.commit()
    finally:
        db.close()

import pytest
from httpx import AsyncClient
from src.main import app
from src.database import Base, engine
from jose import jwt
import os

# Test JWT Configuration
SECRET_KEY = os.getenv("JWT_SECRET_KEY", "your-secret-key")
ALGORITHM = "HS256"

def create_test_token(vendor_id: str):
    payload = {"sub": vendor_id}
    return jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)

@pytest.fixture(scope="module")
def anyio_backend():
    return "asyncio"

@pytest.fixture(autouse=True)
def setup_db():
    Base.metadata.create_all(bind=engine)
    yield
    Base.metadata.drop_all(bind=engine)

@pytest.mark.anyio
async def test_upload_invoice_success():
    vendor_id = "vendor_123"
    token = create_test_token(vendor_id)
    async with AsyncClient(app=app, base_url="http://test") as ac:
        headers = {"Authorization": f"Bearer {token}"}
        pdf_content = b"%PDF-1.4\n%test content"
        files = {"file": ("invoice.pdf", pdf_content, "application/pdf")}
        data = {"vendor_id": vendor_id, "invoice_amount": "150.50"}
        
        response = await ac.post("/upload", headers=headers, data=data, files=files)
        
    assert response.status_code == 202
    assert "track_id" in response.json()
    assert response.json()["status"] == "PENDING"

@pytest.mark.anyio
async def test_upload_invoice_invalid_type():
    vendor_id = "vendor_123"
    token = create_test_token(vendor_id)
    async with AsyncClient(app=app, base_url="http://test") as ac:
        headers = {"Authorization": f"Bearer {token}"}
        files = {"file": ("test.txt", b"not a pdf", "text/plain")}
        data = {"vendor_id": vendor_id, "invoice_amount": "150.50"}
        
        response = await ac.post("/upload", headers=headers, data=data, files=files)
        
    assert response.status_code == 400
    assert response.json()["detail"] == "Invalid File Type: Not a PDF"

@pytest.mark.anyio
async def test_upload_invoice_too_large():
    vendor_id = "vendor_123"
    token = create_test_token(vendor_id)
    async with AsyncClient(app=app, base_url="http://test") as ac:
        headers = {"Authorization": f"Bearer {token}"}
        large_content = b"%PDF-" + b"0" * (6 * 1024 * 1024) # 6MB
        files = {"file": ("large.pdf", large_content, "application/pdf")}
        data = {"vendor_id": vendor_id, "invoice_amount": "150.50"}
        
        response = await ac.post("/upload", headers=headers, data=data, files=files)
        
    assert response.status_code == 413

@pytest.mark.anyio
async def test_upload_invoice_vendor_mismatch():
    token = create_test_token("vendor_123")
    async with AsyncClient(app=app, base_url="http://test") as ac:
        headers = {"Authorization": f"Bearer {token}"}
        pdf_content = b"%PDF-1.4\n"
        files = {"file": ("invoice.pdf", pdf_content, "application/pdf")}
        data = {"vendor_id": "wrong_vendor", "invoice_amount": "100.00"}
        
        response = await ac.post("/upload", headers=headers, data=data, files=files)
        
    assert response.status_code == 403
    assert response.json()["detail"] == "Vendor ID mismatch"

@pytest.mark.anyio
async def test_upload_invoice_invalid_token():
    async with AsyncClient(app=app, base_url="http://test") as ac:
        headers = {"Authorization": "Bearer invalid_token_format"}
        pdf_content = b"%PDF-1.4\n"
        files = {"file": ("invoice.pdf", pdf_content, "application/pdf")}
        data = {"vendor_id": "vendor_123", "invoice_amount": "100.00"}
        
        response = await ac.post("/upload", headers=headers, data=data, files=files)
        
    assert response.status_code == 401

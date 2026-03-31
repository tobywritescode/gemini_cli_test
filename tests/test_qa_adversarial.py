import pytest
import asyncio
from httpx import AsyncClient
from src.main import app
from src.database import Base, engine
from jose import jwt
import os

# Test Configuration
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
async def test_stress_concurrency():
    """Property-based stress test: Handle 20 concurrent uploads."""
    vendor_id = "concurrent_vendor"
    token = create_test_token(vendor_id)
    headers = {"Authorization": f"Bearer {token}"}
    pdf_content = b"%PDF-1.4\n" + b"x" * 1024
    
    async def upload_task(i):
        async with AsyncClient(app=app, base_url="http://test") as ac:
            data = {"vendor_id": vendor_id, "invoice_amount": str(10.00 + i)}
            files = {"file": (f"invoice_{i}.pdf", pdf_content, "application/pdf")}
            return await ac.post("/upload", headers=headers, data=data, files=files)

    results = await asyncio.gather(*[upload_task(i) for i in range(20)])
    
    for resp in results:
        assert resp.status_code == 202
        assert resp.json()["status"] == "PENDING"

@pytest.mark.anyio
async def test_boundary_file_size_limit():
    """Edge Case: Exactly 5MB should pass, 5MB + 1 byte should fail."""
    vendor_id = "vendor_123"
    token = create_test_token(vendor_id)
    headers = {"Authorization": f"Bearer {token}"}
    
    # 5MB exactly
    exact_5mb = b"%PDF-" + b"0" * (5 * 1024 * 1024 - 5)
    async with AsyncClient(app=app, base_url="http://test") as ac:
        data = {"vendor_id": vendor_id, "invoice_amount": "100.00"}
        files = {"file": ("exact.pdf", exact_5mb, "application/pdf")}
        resp_pass = await ac.post("/upload", headers=headers, data=data, files=files)
    
    # 5MB + 1 byte
    over_5mb = exact_5mb + b"1"
    async with AsyncClient(app=app, base_url="http://test") as ac:
        data = {"vendor_id": vendor_id, "invoice_amount": "100.00"}
        files = {"file": ("over.pdf", over_5mb, "application/pdf")}
        resp_fail = await ac.post("/upload", headers=headers, data=data, files=files)

    assert resp_pass.status_code == 202
    assert resp_fail.status_code == 413

@pytest.mark.anyio
async def test_fuzz_malformed_magic_bytes():
    """Fuzzing: Various malformed PDF headers."""
    vendor_id = "vendor_123"
    token = create_test_token(vendor_id)
    headers = {"Authorization": f"Bearer {token}"}
    
    malformed_headers = [
        b"%PD-",       # Incomplete
        b"PDF-1.4",    # Missing percent
        b"\x00%PDF-",  # Null prefix
        b"         ",  # Empty
    ]
    
    async with AsyncClient(app=app, base_url="http://test") as ac:
        for content in malformed_headers:
            data = {"vendor_id": vendor_id, "invoice_amount": "10.00"}
            files = {"file": ("bad.pdf", content, "application/pdf")}
            resp = await ac.post("/upload", headers=headers, data=data, files=files)
            assert resp.status_code == 400
            assert resp.json()["detail"] == "Invalid File Type: Not a PDF"

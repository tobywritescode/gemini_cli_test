# Interfaces and Component Boundaries

## API Interface (FastAPI/Pydantic)

### Endpoint: `POST /upload`
- **Authentication**: OAuth2 (Bearer Token)
- **Content-Type**: `multipart/form-data`

### Request Parameters
| Field | Type | Description |
| :--- | :--- | :--- |
| `vendor_id` | `str` | Unique vendor identifier |
| `invoice_amount` | `Decimal` | Total invoice amount |
| `file` | `UploadFile` | PDF file (max 5MB) |

### Response Models
```python
from pydantic import BaseModel
from uuid import UUID

class UploadResponse(BaseModel):
    track_id: UUID
    status: str = "PENDING"
    message: str = "Invoice upload initiated."
```

## Component Boundaries

### 1. Synchronous Validation Layer
- **OAuth2 Validation**: Verify vendor token.
- **Magic Byte Check**: Verify file header starts with `%PDF-`.
- **Size Constraint**: Enforce 5MB limit at the gateway/application level.

### 2. Persistence Layer
- **PostgreSQL**: Stores metadata and tracks upload lifecycle state.

### 3. Asynchronous Layer
- **Task Queue**: Offloads high-latency S3 IO operations.
- **Worker**: Handles cloud storage communication and final status updates.

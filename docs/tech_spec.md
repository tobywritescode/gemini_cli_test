# Technical Specification: Invoice Upload Microservice

## Project Scope
Development of a Python/FastAPI microservice for secure, asynchronous PDF invoice uploads. The system will validate file integrity, store metadata in PostgreSQL, and offload the file to cloud storage (S3-compatible).

## 1. Gherkin Scenarios

### Scenario: Successful Asynchronous Invoice Upload
- **GIVEN** a registered vendor with a valid OAuth2 token
- **AND** a valid PDF file under 5MB
- **AND** valid metadata (Vendor ID, Invoice Amount)
- **WHEN** the vendor submits a POST request to the `/upload` endpoint
- **THEN** the system returns a `202 Accepted` status with a unique `track_id`
- **AND** the file is queued for background processing to cloud storage
- **AND** the metadata is persisted in the PostgreSQL database.

### Scenario: Rejection of Oversized File
- **GIVEN** an authenticated vendor
- **WHEN** they attempt to upload a file larger than 5MB
- **THEN** the system returns a `413 Request Entity Too Large` error
- **AND** no background processing is initiated.

### Scenario: Rejection of Invalid File Type
- **GIVEN** an authenticated vendor
- **WHEN** they upload a non-PDF file (e.g., `.exe` or `.png`)
- **THEN** the system returns a `400 Bad Request` with an "Invalid File Type" error message.

### Scenario: Unauthorized Access
- **GIVEN** an unauthenticated user or an invalid OAuth2 token
- **WHEN** they attempt to access the `/upload` endpoint
- **THEN** the system returns a `401 Unauthorized` error.

## 2. Data Dictionary

| Field | Type | Constraint | Description |
| :--- | :--- | :--- | :--- |
| `vendor_id` | UUID / String | Required, Non-empty | Unique identifier for the vendor. |
| `invoice_amount` | Decimal | Required, Positive | The total amount on the invoice. |
| `file` | Binary (PDF) | Required, Max 5MB | The invoice document in PDF format. |
| `track_id` | UUID | System Generated | Identifier to track the status of the async upload. |
| `created_at` | Timestamp | System Generated | Record creation time in UTC. |
| `status` | String | Enum | Status of the upload (e.g., PENDING, COMPLETED, FAILED). |

## 3. Edge Cases & Constraints
- **Malware Prevention:** The system must perform a "magic byte" check to verify the file is a true PDF.
- **Queue Failures:** If the background task fails, the system must mark the record as `failed` in the database.
- **Concurrent Uploads:** The system must handle multiple simultaneous uploads without metadata corruption.

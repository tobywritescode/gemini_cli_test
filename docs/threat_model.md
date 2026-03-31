# Threat Model: Invoice Upload Microservice

## 1. Trust Boundary Map
- **Boundary A (External/Untrusted):** Public Internet to FastAPI Application.
- **Boundary B (Internal/Trusted):** FastAPI Application to PostgreSQL and Task Queue (Redis).
- **Boundary C (Internal/Trusted):** Background Worker to Cloud Storage (S3).

## 2. Threat Analysis (STRIDE)

| Threat Type | Attack Vector | Mitigation Mandate |
| :--- | :--- | :--- |
| **Spoofing** | Attacker impersonates a vendor using stolen or forged credentials. | **Mandate:** Strict OAuth2 JWT validation with signature and expiration checks. |
| **Tampering** | Attacker uploads a malicious script disguised as a PDF or modifies metadata. | **Mandate:** "Magic byte" verification (`%PDF-`) and 5MB size limit enforced *before* processing. |
| **Repudiation** | Vendor denies an invoice upload or its contents. | **Mandate:** Comprehensive audit logging (Vendor ID, Timestamp, Track ID, File Hash) in PostgreSQL. |
| **Information Disclosure** | Unauthorized access to metadata or invoice files. | **Mandate:** Encryption at rest for PostgreSQL and S3 (AES-256). All transit via TLS 1.3. |
| **Denial of Service** | Resource exhaustion via massive file uploads or rapid API calls. | **Mandate:** API Rate Limiting and strict file size enforcement at the gateway/application level. |
| **Elevation of Privilege** | Vendor A attempts to read or overwrite Vendor B's invoices. | **Mandate:** Row-level security or strict filtering by `vendor_id` (extracted from OAuth2 token) in all queries. |

## 3. Security Mandates
- **Input Sanitization:** Reject any file not meeting the PDF header specification.
- **Storage Security:** S3 buckets must be private with no public access. Files must only be accessible via time-limited pre-signed URLs.
- **Data Protection:** Personally Identifiable Information (PII) within metadata must be minimized.
- **Infrastructure:** Use IAM roles for worker-to-S3 communication; no hardcoded credentials.

# Test Evidence: Invoice Upload Microservice

## 1. QA Test Scenarios (Phase 6)

| Test ID | Category | Description | Result |
| :--- | :--- | :--- | :--- |
| **QA-ADV-01** | **Stress** | Handle 20 concurrent uploads without race conditions or failures. | **PASSED** |
| **QA-ADV-02** | **Boundary** | Verify exact 5.0MB pass and 5.0MB + 1 byte rejection (HTTP 413). | **PASSED** |
| **QA-ADV-03** | **Fuzz** | Reject files with malformed magic bytes (e.g., missing `%`, null prefixes). | **PASSED** |

## 2. Functional Test Scenarios (Phase 4)

| Test ID | Description | Result |
| :--- | :--- | :--- |
| **FUNC-01** | Successful PDF upload with valid metadata and OAuth2 token. | **PASSED** |
| **FUNC-02** | Rejection of non-PDF file types. | **PASSED** |
| **FUNC-03** | Rejection of file sizes significantly over the 5MB limit. | **PASSED** |
| **FUNC-04** | Enforcement of Vendor ID ownership (RBAC check). | **PASSED** |
| **SEC-VAL-01**| Rejection of invalid/unauthorized JWT tokens. | **PASSED** |

## 3. Execution Summary
- **Total Tests**: 8
- **Pass Rate**: 100%
- **Environment**: Python 3.12 (Poetry) / SQLite (Test) / FastAPI
- **Evidence Timestamp**: March 31, 2026

## Conclusion
The microservice is functionally complete and has passed adversarial stress tests designed to violate its boundaries. The system maintains state integrity under load and correctly enforces all security mandates.

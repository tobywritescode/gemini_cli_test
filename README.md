# Invoice Upload Microservice

A secure, asynchronous microservice built with Python and FastAPI for external vendors to upload PDF invoices. The system validates file integrity, enforces size limits, and stores metadata in PostgreSQL while offloading the file to cloud storage.

## Purpose
This service provides a secure entry point for financial documents, ensuring that:
1. Only authenticated vendors can upload files.
2. Only valid PDF documents under 5MB are accepted.
3. The upload process is non-blocking (asynchronous) for high performance.
4. All actions are audited with metadata tracking and integrity checks.

## Tech Stack
- **Framework:** FastAPI (Python 3.10+)
- **Database:** PostgreSQL (SQLAlchemy 2.0 ORM)
- **Task Queue:** FastAPI BackgroundTasks
- **Auth:** OAuth2 with JWT validation (`python-jose`)
- **Package Manager:** Poetry

## SDLC Project Summary

### 1. Technical Mapping
The final implementation strictly maps to the approved `docs/tech_spec.md`.
- **Status Codes:** `202 Accepted` (Async), `413` (Size Limit), `400` (Invalid Type), `401/403` (Auth).
- **Security:** Implements "Magic Byte" verification (`%PDF-`) and strict JWT signature checks.
- **Asynchronous Flow:** Uses FastAPI `BackgroundTasks` to offload S3 I/O.

### 2. SDLC Execution Metrics
- **Refactor Cycles:** 3 major refactors (TDD integration, Security hardening, and Modern FastAPI patterns).
- **Final Test Pass Rate:** 100% (8/8 tests).

### 3. Challenges & Remediation
- **Packaging:** Resolved Poetry installation errors by setting `package-mode = false`.
- **Imports:** Fixed `ModuleNotFoundError` by implementing absolute imports and `src/__init__.py`.
- **Security:** Addressed mocked authentication findings by implementing actual JWT validation and strict environment variable enforcement.

## Getting Started

### Installation
Ensure you have [Poetry](https://python-poetry.org/) installed, then run:
```bash
poetry install --no-root
```

### Running Tests
To verify the application, run the full suite (Functional, Security, and Adversarial Stress tests):

```bash
JWT_SECRET_KEY=your-secret-key DATABASE_URL=sqlite:///./test.db PYTHONPATH=. poetry run pytest tests/
```

### Project Structure
- `src/`: Core application logic (main, models, schemas, tasks).
- `tests/`: TDD and QA Adversarial test suites.
- `docs/`: Technical specifications, architecture diagrams, and security audits.

---
**Status: Verified & Concluded**

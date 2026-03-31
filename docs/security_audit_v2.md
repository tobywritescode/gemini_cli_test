# Security Audit Report v2: Invoice Upload Microservice

## New Observations & Technical Debt

| ID | Severity | Location | Vulnerability Type | Description | Remediation |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **SEC-05** | **Informational** | `src/main.py` | **Technical Debt** | `@app.on_event("startup")` is deprecated in FastAPI. | Migrate to using `contextlib.asynccontextmanager` for `lifespan` handlers. |
| **SEC-06** | **Low** | `src/dependencies.py` | **Configuration Risk** | `SECRET_KEY` defaults to a hardcoded string if the environment variable is missing. | Raise a `RuntimeError` if `JWT_SECRET_KEY` is not set in the environment. |

## Audit Conclusion
The core security issues (Auth/Integrity) are resolved. These final changes will ensure the application uses the latest FastAPI patterns and enforces strict configuration safety.

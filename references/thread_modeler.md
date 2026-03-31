# MODULE: Structural Threat Analyzer

## DEFINITION
A proactive security engine that evaluates architectural designs and data models to identify structural vulnerabilities, trust boundary violations, and missing mitigations (e.g., using methodologies like STRIDE).

## THE TRANSFORMATION
- **Input:** Approved Architecture Diagrams, Interface Definitions, Data Models, and Target Tech Stack.
- **Output:** A formal Threat Model document, explicit Trust Boundary maps, and a list of mandated security controls (e.g., specific Authn/Authz requirements, encryption standards).

## SEMANTIC CONTRACT (CONSTRAINTS)
- The module must map specific attack vectors directly to the provided data flows. It must reject generating generic security advice.
- Assumptions regarding network safety must be zero (Zero Trust).
- Distinctions between public, internal, and privileged data must be made explicit.

## AUTHORITY BOUNDARY
- **ALLOWED:** Mandate specific cryptographic standards, define RBAC (Role-Based Access Control) boundaries, and reject architectures that leak sensitive data.
- **FORBIDDEN:** Alter the core business requirements, write implementation code, or accept business risk for identified vulnerabilities.
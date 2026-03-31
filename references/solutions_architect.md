# MODULE: Architecture & Interface Synthesizer

## DEFINITION
A pattern-projection engine that translates verified functional requirements into structural boundaries, data models, and interface definitions for the target technology stack.

## THE TRANSFORMATION
- **Input:** Verified Technical Specifications (Gherkin scenarios, non-functional requirements) and the declared target technology stack.
- **Output:** Architecture diagrams (e.g., Mermaid.js), strict interface definitions (using the target language's native interface/trait/protocol paradigms), strictly typed data models, and structural Threat Models.

## SEMANTIC CONTRACT (CONSTRAINTS)
- [cite_start]The output must encode intent and constraint rather than outcome alone[cite: 61].
- Interfaces must enforce strict typing appropriate for the chosen language (no dynamic/any types unless explicitly required by the domain).
- Designs must proactively account for concurrency constraints (e.g., race conditions, deadlocks) and explicitly map data flow boundaries.

## AUTHORITY BOUNDARY
- **ALLOWED:** Define inputs, outputs, data models, and security mitigations in the design.
- **FORBIDDEN:** Write implementation logic (method bodies), dictate business trade-offs (e.g., sacrificing data consistency for speed), or finalize tech-stack decisions without human approval.
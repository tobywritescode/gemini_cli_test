# MODULE: Adversarial Edge-Case Generator

## DEFINITION
A bounded stress-testing engine designed to generate programmatic inputs that violate expected system boundaries, focusing on property-based and fuzz testing using frameworks native to the target tech stack.

## THE TRANSFORMATION
- **Input:** Completed Implementation Code, Interface Definitions, Data Models, and the declared target technology stack.
- **Output:** Test scripts utilizing appropriate native libraries to flood the system with malformed data, concurrency stress tests, and boundary value violations.

## SEMANTIC CONTRACT (CONSTRAINTS)
- The module must target invariant properties rather than standard "Happy Path" equality checks (e.g., testing that state is preserved under load, not just that X + Y = Z).
- Outputs must include explicit reproduction steps for any generated failure states.

## AUTHORITY BOUNDARY
- **ALLOWED:** Generate infinite loops, massive payload simulations, malformed data structures, and flag stack-trace leaks.
- **FORBIDDEN:** Rewrite or "fix" the implementation code, assess the acceptable business risk of a failure, or authorize a release.
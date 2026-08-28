---
name: governance-verification
description: Use only when risk or an event requires evidence review, independent audit, finding closure, or governance review.
---

# governance-verification

This is not a default step for `LOW` risk work. Low Risk with no Finding or
Runtime Boundary to `SKIP`; route `MEDIUM`/`HIGH` or a triggered event to
`EXECUTE`. Missing required authorization or evidence routes to `STOP`.

## Conditional checks

- Evidence: distinguish requested, actual, and persistent evidence.
- Independent Audit: require a separate read-only reviewer only when triggered.
- Finding Closure: require identity, remediation evidence, re-verification, residual risk, and closure decision only when a finding exists.
- Governance Review: summarize scope, permission, result, evidence, findings, and runtime record.

Return `PASS`, `PASS WITH OBSERVATIONS`, `INCONCLUSIVE`, `FAIL`, or `NOT COMPLETED`. Do not fix findings, grant authorization, expose secrets, or advance lifecycle state.

---
name: governance-preflight
description: Use before work that may change scope, permission, or protected boundaries; keep low-risk checks minimal.
---

# governance-preflight

For ordinary `LOW`, bounded, reversible work, perform only:

`Scope → Authorization → Risk → Protected Action`

Do not load history, migration records, Feature Parity, or full standards by default. Use `LOW`, `MEDIUM`, `HIGH`, or `UNKNOWN`; `UNKNOWN` returns `INCONCLUSIVE` and `STOP`. Escalate only when risk is medium/high, scope is ambiguous, or a protected action is present.

## Role and permission economy

`Model ≠ Role ≠ Permission`. A LOW-risk single Builder task (Low Risk) does not require
Architect/Builder/Auditor records. Expand role records only for Role change,
Permission escalation, Independent Audit, Handoff, or Multi-Agent delegation.

## Output

Return `AUTHORIZED`, `NOT AUTHORIZED`, or `INCONCLUSIVE`, with the declared scope, risk, protected action status, evidence references, and stop condition when applicable.

## Escalation

Trigger `governance-verification` for complex evidence, runtime or external boundaries, findings, or requested independent audit. Trigger `secret-protection-review` for sensitive values or data. Trigger `production-readiness-review` for production, deployment, release, real users, or customer data.

Never grant human authorization, infer runtime behavior, expose secrets, or advance lifecycle state.

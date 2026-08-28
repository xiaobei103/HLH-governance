# HLH Governance Policy

## Ownership

HLH owns Governance: Authorization, Scope, Permission, Risk, Stop Conditions,
Evidence Requirements, Human Decision Gates, Finding Closure, Completion
Decision, Production Readiness Decision, Handoff Gate, and Commit-only
Authorization. Engineering execution is replaceable and may be supplied by
Superpowers or another compliant layer.

## State separation

Authorization, Execution, Verification, Completion, Commit, and Production
Readiness are separate states. A later state must never be inferred from an
earlier state.

## Evidence states

Use only `PASS`, `PASS WITH OBSERVATIONS`, `INCONCLUSIVE`, `FAIL`, or
`NOT COMPLETED`. Requested Runtime Evidence, Actual Runtime Evidence, and
Persistent Runtime Evidence must be distinguished.

## Protected actions

Writes, commits, pushes, tags, deployment, production access, external-account
actions, real customer data, secrets, and irreversible operations require an
explicit scope and the applicable human authorization. Commit is never included
in Builder Write Authority; it requires independent Commit-only Authorization.

## Hook evidence

Hook claims require evidence for Official Capability, Configuration Discovery,
Trigger, Behavior, Boundary, Persistence, and Rollback. Missing any layer means
`INCONCLUSIVE`.

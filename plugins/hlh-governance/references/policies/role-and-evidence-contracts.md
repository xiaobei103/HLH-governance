# HLH Governance Contracts

## Model, Capability, Role, Permission

These are separate fields and must never be inferred from one another.

- **Model**: runtime model configuration; record requested and actual model only.
- **Capability**: what runtime can technically do; it does not grant permission.
- **Lifecycle Role**: Architect, Builder, or Auditor; it defines responsibility and default authority.
- **Specialty Role**: Coding, Testing, Security, Deployment, or Monitoring; it defines domain only.
- **Permission**: user-authorized operation boundary, such as Read-only or scope-limited Write Authority.

Role is not authorization. Capability is not permission. Model is not role. Every role transition requires a new Role, Scope, Permission, and Authorization record.

## Single Write Authority

For one repository, Work Package, and time window, at most one Builder may hold Write Authority. Architect and Auditor are read-only by default. Specialty Role never grants write permission. Builder Write Authority covers only the explicitly authorized scope. Git add, commit, push, tag, deployment, production access, and irreversible actions remain separately protected. On scope expansion, concurrent writers, or Builder/Auditor conflict: STOP. Before handoff or completion, Write Authority is released and Git state is captured.

## Handoff Gate

A handoff passes seven gates: outgoing Builder releases Write Authority; Git captures HEAD, branch, status, staged and untracked files; a state record identifies Work Package, owner, scope and state; the summary lists completed work, incomplete work, risks, evidence and next action; the incoming agent validates Git state; the user re-authorizes incoming Role, Scope, Permission and Authorization; then the incoming agent starts.

Clean Handoff requires a clean working tree and committed state. Controlled Dirty Handoff is allowed only when every uncommitted change records File, Status, Owner, Work Package, Reason and Action. Staged is not clean. Incomplete handoff stops.

## Completion and delegation

The Main Agent owns the current Work Package Completion Decision. Subagents provide bounded results and evidence but cannot claim final completion, close their own findings, change lifecycle state, infer Production Readiness, or commit without independent Commit-only Authorization.

A delegation record declares task, scope, lifecycle role, specialty role, permission, owner, expected output and stop conditions. Subagents have no implicit Write Authority. Only one Builder may write. Auditor is independent from Builder and read-only; an agent cannot audit its own implementation in the same Work Package.

## Risk and evidence

Classify risk before execution: R0 read-only/no external effect, R1 bounded local change, R2 protected action or sensitive boundary, R3 irreversible/production/external side effect. Unknown risk is INCONCLUSIVE and stops.

Self-Verify records scope, checks, result, incomplete items and evidence limits. Finding Closure records finding ID, original condition, remediation, verification evidence, residual risk and closure decision. Runtime records distinguish Requested Model/Reasoning/Capability from Actual Model/Reasoning/Capability; unknown actual values are INCONCLUSIVE. Tests alone are not runtime evidence.

Execution Result Governance Review receives declared scope, role, permission, result, evidence, findings and runtime record. It can return PASS, PASS WITH OBSERVATIONS, INCONCLUSIVE or FAIL, but cannot execute fixes or grant authorization.

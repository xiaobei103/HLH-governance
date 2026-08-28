---
name: delivery-decision
description: Use at the delivery boundary to evaluate self-verification and completion; add commit or handoff checks only when requested.
---

# delivery-decision

The normal delivery path is Self-Verify followed by a completion decision. Keep completion, commit, and production readiness separate.

## Conditional checks

- Require scope, checks, result, incomplete items, and evidence limits for Self-Verify.
- Reconcile `Declared Scope`, `Authorized Scope`, `Actual Change`, and
  `Verified Result` before Completion.
- Report `Incomplete Items`, `Out-of-Scope Observations`, and `Next Authorized
  Action` (Next Authorized Action); incomplete requirements are `INCOMPLETE`
  and do not permit Completion.
- Apply Commit-only Authorization only when a commit is requested or proposed.
- Apply Handoff only when work crosses agents, worktrees, phases, or owners.
- Do not infer Production Readiness; invoke `production-readiness-review` only for production or release scenarios.

Completion does not imply Commit (`Completion != Commit`), and Commit does not
imply Production Readiness (`Commit != Production Readiness`). Never commit,
grant authorization, expand scope, or advance lifecycle state.

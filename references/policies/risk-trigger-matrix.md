# HLH v3.2 Risk Trigger Matrix

This matrix is the runtime entry contract. It keeps low-risk work short and
expands governance only when risk or an event requires it.

| Risk or event | Required path |
|---|---|
| `LOW`: bounded, reversible local change | `governance-preflight → EXECUTE → Self-Verify → delivery-decision` |
| `MEDIUM`: evidence review or runtime/external boundary | `governance-verification → EXECUTE` |
| `HIGH`: production/deployment/release or high-impact boundary | required specialist review → `EXECUTE` |
| Secret, credential, token, PII, sensitive output, diff, log, fixture, or evidence | `secret-protection-review → EXECUTE` |
| Production, deployment, release, real user, or customer data | `production-readiness-review → EXECUTE` |
| Commit requested or proposed | Add commit-only check inside `delivery-decision` |
| Agent, worktree, phase, or owner transition | Add handoff check inside `delivery-decision` |
| `UNKNOWN` or ambiguous risk | `INCONCLUSIVE → STOP`; do not guess or run the full chain automatically |

Persistent Evidence, Independent Audit, and Finding Closure are conditional
subflows of `governance-verification`, not default low-risk requirements.

# Trusted Evidence Model

| Evidence state | Meaning |
|---|---|
| `STATIC_DISCOVERY` | Files, manifest, or configuration were inspected. |
| `SYNTHETIC_TEST` | A controlled test exercised local logic or validation. |
| `ACTUAL_INVOCATION` | The target Skill, script, or command was invoked. |
| `ACTUAL_RUNTIME_EVIDENCE` | Invocation, matcher, handler, decision, and runtime outcome are correlated. |
| `INCONCLUSIVE` | Required evidence was unavailable; no capability is inferred. |

Command success is not Hook allow evidence, and command failure is not Hook deny evidence. A commit is not Completion, and Completion is not Production Readiness.

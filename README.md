# HLH Governance Plugin

This repository is the HLH v3.2 Governance Plugin. It governs authorization,
scope, protected actions, evidence, independent audit, finding closure,
completion, production readiness, handoff, commit-only authorization, and
secret protection.

HLH is execution-layer independent. Superpowers and Codex may provide
brainstorming, planning, TDD, debugging, worktrees, subagents, implementation,
testing, and ordinary code review; HLH does not duplicate those capabilities.

## Risk-based path

Runtime context is minimal by default: always load only the current Skill,
trigger matrix, execution boundary, Scope, Authorization, and Protected Action
status. Load evidence and specialist Skills conditionally by risk and event;
history, migration, Feature Parity, full standards, and unrelated evidence are
never default context. The public risk interface is `LOW`, `MEDIUM`, `HIGH`,
or `UNKNOWN`; unknown risk returns `INCONCLUSIVE` and `STOP`.

Low-risk bounded and reversible work uses the shortest path:

`governance-preflight → Execution → Self-Verify → delivery-decision`

`governance-verification` is conditional for medium/high risk, runtime or
external boundaries, complex evidence, findings, or an explicitly requested
independent audit. `secret-protection-review` is conditional for sensitive
values or data. `production-readiness-review` is conditional for production,
deployment, release, real users, or customer data.

The complete trigger contract is in
`references/policies/risk-trigger-matrix.md`. Historical sources and migration
records remain preserved and are not part of the low-risk default path.

## Active Runtime

The Active Runtime Authority is `skills/entries/**`, with exactly these five
Active Skills:

- `governance-preflight`
- `governance-verification`
- `delivery-decision`
- `secret-protection-review`
- `production-readiness-review`

The `references/policies/**` and `references/standards/**` directories provide
repo-local governance rules and standards. `scripts/**` provides validation and
evidence utilities, while `tests/**` provides synthetic regression coverage.
The Plugin is standalone and has no runtime dependency on the legacy Workflow
repository. That repository remains the Legacy / Historical Source Repository
for provenance and retained historical evidence.

MCP, MCP Servers, and App integrations are excluded from the v3.2 Plugin
Runtime by design.

Optional validation tools provide metadata-only Context Usage Evidence and a
minimal Governance State for resume across handoff or threads. They record
references and decisions, never context bodies; LOW Risk persistence is
optional and validation/debug oriented. See
`references/policies/minimal-governance-context.md` and
`references/policies/governance-state-contract.md`.

## Status

Phase 0–4 packaging assets are present. A synchronous, protected-action-only
PreToolUse Hook candidate is bundled for capability validation; PostToolUse,
SessionStart, async hooks, and lifecycle decision hooks are intentionally not
included. Hook implementation is present, but Plugin Hook Runtime Validation
remains INCONCLUSIVE until a trusted Desktop/Runtime trigger is captured. The
Hook capability is OPTIONAL / RUNTIME-DEPENDENT.
numbered legacy directories remain during migration and are not yet deprecated
or deleted. Feature Parity and Runtime Verification are still required before
decommissioning legacy runtime copies.

## Runtime rule

Never infer authorization, completion, production readiness, or Hook execution
from configuration existence, a model statement, a successful test alone, or
a commit. Use the relevant Skill and record actual evidence.

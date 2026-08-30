# HLH Governance

Evidence-driven governance controls for AI-assisted software engineering.

HLH Governance is a Codex Plugin for teams that want clear boundaries around
authorization, scope, protected actions, evidence, audit, completion, and
production readiness while using AI coding agents.

It is a governance control layer—not a complete engineering workflow.

## Why use HLH Governance?

AI-assisted development can make changes quickly, but “the agent said it is
done” is not the same as authorized, verified, complete, or production-ready.
HLH keeps those states explicit:

```text
Authorization ≠ Execution ≠ Verification ≠ Completion ≠ Commit ≠ Production Readiness
```

This gives a development team a shared language for deciding what may happen,
what actually happened, what evidence exists, and what still needs review.

## What it controls

- Risk-based governance routing: `LOW`, `MEDIUM`, `HIGH`, and `UNKNOWN`.
- Scope and authorization boundaries.
- Protected actions such as destructive operations and Git publishing actions.
- Evidence, independent audit, finding closure, and delivery decisions.
- Secret-protection review when output, logs, diffs, fixtures, or data may be sensitive.
- Production-readiness review for release, deployment, real users, or customer data.

## Installation

The following is the verified public GitHub marketplace installation path:

```bash
codex plugin marketplace add https://github.com/xiaobei103/HLH-governance
codex plugin add hlh-governance@hlh-governance
```

The marketplace source is the public repository:

```text
https://github.com/xiaobei103/HLH-governance
```

After installation, confirm that `hlh-governance` is installed and enabled in
Codex before starting the Quick Start flow.

## Quick Start

### 1. Start a fresh Codex thread

Use a fresh thread after installation so the Plugin and its Skills are loaded
from the current Codex environment.

### 2. Run the shortest governance path

For bounded, reversible work, invoke:

```text
governance-preflight
```

Declare the task scope, authorization, risk, and whether a protected action is
involved. A typical low-risk flow is:

```text
governance-preflight
→ bounded execution
→ self-verify
→ delivery-decision
```

Then invoke `delivery-decision` to distinguish the declared scope, actual
change, verified result, incomplete items, and next authorized action.

### 3. Trigger specialist reviews when applicable

Use the other Active Skills only when their conditions apply:

- `governance-verification` — evidence review, runtime or external boundaries,
  findings, or an explicitly requested independent audit.
- `secret-protection-review` — secrets, credentials, tokens, PII, sensitive
  output, logs, diffs, fixtures, or evidence may be involved.
- `production-readiness-review` — production, deployment, release, real users,
  or customer data are in scope.

If risk or scope is unknown, the correct result is `INCONCLUSIVE → STOP`; do
not guess or silently run a broader workflow.

### 4. Understand the protected-action boundary

The Plugin includes a synchronous PreToolUse Hook candidate for protected
actions. Its package and handler paths are verified, but real Desktop/Runtime
Hook enforcement is not yet verified. The safe interpretation is:

```text
Capability Status: Experimental
Verification Status: INCONCLUSIVE / Not Verified
Runtime Dependency: Runtime-dependent
```

Do not treat a protected-equivalent demonstration, a static manifest check, or
a passing test as proof that a real Hook always blocks an action.

## Five Active Skills

| Skill | Capability Status | Verification Status | Purpose |
|---|---|---|---|
| `governance-preflight` | `Supported` | `PASS` | Scope, authorization, risk, and protected-action preflight |
| `governance-verification` | `Supported` | `PASS` | Evidence review, audit, findings, and runtime-boundary review |
| `delivery-decision` | `Supported` | `PASS` | Completion, delivery, handoff, and commit boundary decisions |
| `secret-protection-review` | `Supported` | `PASS` | Safe handling of secrets, credentials, PII, and sensitive evidence |
| `production-readiness-review` | `Supported` | `PASS` | Production, deployment, release, and real-user readiness review |

## Capability status

The public capability model has four states:

- `Supported` — implemented and covered by current verification evidence.
- `Experimental` — available but stability or runtime evidence remains limited.
- `Not Verified` — evidence is not sufficient to make a stronger claim.
- `Not Supported` — outside the current supported scope.

| Capability | Status |
|---|---|
| Five Active Skills | `Supported` / verification `PASS` |
| Hook package and path resolution | `Supported` as package structure; runtime enforcement remains `Experimental` / `INCONCLUSIVE` |
| Claude Code | `Not Supported` |
| Cursor | `Not Supported` |
| MCP integrations | `Not Supported` in the v3.2 Plugin Runtime |
| SaaS or Web Console | `Not Supported` |

## What HLH does not replace

HLH does not replace planning, TDD, debugging, implementation, ordinary code
review, operating-system sandboxing, identity and access control, network
isolation, or human approval. Codex and other execution-layer tools may provide
those capabilities; HLH defines governance boundaries around them.

HLH also does not make an unverified Hook runtime production-ready. Production
readiness remains a separate decision with separate evidence.

## Typical governance flow

```text
Claim
→ Evidence
→ Self-Verify
→ Independent Audit (when triggered)
→ Finding Closure (when required)
→ Completion Decision
→ Production Readiness Decision (when applicable)
→ Commit-only Authorization
```

Tests, a clean working tree, a commit, or a model statement do not by
themselves prove later states in this chain.

## Repository structure

```text
HLH-governance/
├── .agents/plugins/marketplace.json
├── plugins/hlh-governance/
│   ├── .codex-plugin/plugin.json
│   ├── skills/entries/
│   ├── hooks.json
│   ├── hooks/
│   ├── references/
│   └── scripts/
├── tests/
├── README.md
├── CHANGELOG.md
└── LICENSE
```

The five Active Skills are under
`plugins/hlh-governance/skills/entries/`. Governance references and validation
scripts are under `plugins/hlh-governance/references/` and
`plugins/hlh-governance/scripts/`.

## Verification status

The public repository has verified:

- Public GitHub marketplace discovery and clean Plugin installation.
- Plugin manifest parsing for version `3.2.0`.
- Discovery of all five Active Skills.
- Hook package path resolution.
- Governance script regression tests and Plugin preflight.

The following remains explicitly unverified:

- Real Codex Desktop/Runtime Hook enforcement.
- Claude Code and Cursor support.
- MCP integration.
- Production deployment or customer-data readiness.

## Contributing

Please include the affected scope, expected behavior, verification evidence,
and known limitations in a contribution or issue. Do not include real
credentials, tokens, private keys, `.env` files, or sensitive user data.

## License

Released under the MIT License. See [LICENSE](LICENSE).

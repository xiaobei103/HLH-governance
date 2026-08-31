# Public Preview
HLH Governance `3.2.0` is a public preview of an evidence-driven governance control layer for AI-assisted software engineering. It is not a complete engineering workflow and is not production-ready software.

## Supported

The five Active Skills are supported with current repository verification:

| Capability | Status |
|---|---|
| `governance-preflight` | Supported / PASS |
| `governance-verification` | Supported / PASS |
| `delivery-decision` | Supported / PASS |
| `secret-protection-review` | Supported / PASS |
| `production-readiness-review` | Supported / PASS |

Installation and quick start are documented in the [README](../../README.md). The marketplace entry, manifest, and public package use version `3.2.0`.

## Unsupported

- Claude Code
- Cursor
- MCP integrations in the v3.2 Plugin Runtime
- SaaS or Web Console operation
- Production deployment, customer-data readiness, or Stable promotion

## Hook limitation

The PreToolUse Hook candidate is statically present, but real Codex Desktop/Runtime lifecycle invocation and enforcement have not been independently established:

```text
Experimental / Runtime-dependent / INCONCLUSIVE
```

A passing unit test, static manifest check, or safe command demonstration is not proof that the live Hook blocks every protected action.

## Evidence and verification status

The automated baseline covers regression tests, plugin preflight, and a secret/privacy scan. These checks support package and repository claims only. They do not establish external service behavior, live Hook enforcement, or production readiness. Claims without sufficient evidence remain `INCONCLUSIVE`.

## Known limitations

- Runtime Hook lifecycle evidence is not available.
- Compatibility is limited to the documented Codex Plugin package/runtime boundary.
- No guarantee is made for third-party agent products or hosted consoles.
- Legacy numbered directories remain subject to parity and decommission review.
- Public preview feedback may change interfaces, documentation, or support boundaries before a stable release.

Use the repository [issue templates](../../.github/ISSUE_TEMPLATE/) and [CONTRIBUTING.md](../../CONTRIBUTING.md). Never publish credentials, private keys, `.env` files, PII, or sensitive logs.

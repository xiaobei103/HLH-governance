# HLH v3.2 Capability Mapping

The five Active Skills are:

- `governance-preflight`
- `governance-verification`
- `delivery-decision`
- `secret-protection-review`
- `production-readiness-review`

Legacy governance capabilities were consolidated into these active entries:
authorization and scope checks into `governance-preflight`; evidence, audit,
and finding review into `governance-verification`; completion and delivery
closure into `delivery-decision`; security-sensitive review into
`secret-protection-review`; and production, release, user, and customer-data
decisions into `production-readiness-review`.

`product-validation-assistant`, `project-architecture-analyzer`,
`scoped-coding-executor`, and `test-acceptance-planner` remain
NON-GOVERNANCE / EXECUTION LAYER capabilities and do not enter the HLH
Governance Runtime.

MCP, MCP Servers, and App integrations are EXCLUDED BY DESIGN. The Hook is
OPTIONAL / RUNTIME-DEPENDENT; Hook Real Runtime Validation remains
INCONCLUSIVE.

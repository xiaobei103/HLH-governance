# Minimal Governance Context Policy

Context Usage Evidence is optional validation/debug metadata. When used, it
records Skill, risk, lifecycle node, reference identifiers, categories, load
reasons, triggers, and timestamp/run ID. It must never copy context bodies or
sensitive values, and it is not required for every ordinary LOW Risk run.

Runtime context is selected by current risk, lifecycle node, and event. A
reference's existence never causes it to load by default.

## Loading semantics

- **Always Load:** current Skill, risk-trigger-matrix, execution-boundary,
  declared Scope, Authorization, and Protected Action status.
- **Conditional Load:** evidence, the directly relevant policy or standard,
  findings, and event-specific specialist Skills only when triggered.
- **Never Default Load:** `references/history/**`, `references/migration/**`,
  Feature Parity, full standards, legacy Skill registries, old-numbered
  Workflow files, and unrelated evidence.

## Risk boundaries

- **LOW:** minimum current-task context; governance-verification defaults to
  `SKIP` when no finding or runtime boundary exists.
- **MEDIUM:** add governance-verification and current evidence or directly
  relevant policy; independent audit, finding closure, secret review, handoff,
  and commit checks remain event-triggered.
- **HIGH:** add only the required production, secret, rollback, monitoring,
  data-protection, runtime-evidence, and stop-condition context.
- **UNKNOWN:** return `INCONCLUSIVE` and route `STOP`; do not auto-load the
  complete governance chain.

Escalate context only for a declared risk/event trigger. History and migration
remain excluded even for HIGH unless a specific historical lookup is authorized.

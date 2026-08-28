# Minimal Governance State Contract

This optional record describes only the current governance position. It is not
an engineering plan, task list, evidence bundle, or workflow state.

Required fields are: `task`, `risk`, `lifecycle_node`, `current_gate`,
`authorization`, `permission`, `evidence_state`, `findings_state`,
`completion_state`, and `next_authorized_action`. `record_type` identifies the
record as `governance-state`.

Resume from the current gate when authorization, scope, permission, risk,
evidence, and protected-action conditions remain valid. Resume from
`next_authorized_action` for `INCOMPLETE`; resume from `finding-closure` when a
finding is present. Any authorization, scope, permission, risk, evidence, or
protected-action change requires `preflight`. `UNKNOWN` is
`INCONCLUSIVE → STOP`.

The record must not contain full history, plans, task lists, evidence bodies,
or engineering workflow state.

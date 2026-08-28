---
name: secret-protection-review
description: Use when output, logs, diffs, evidence, fixtures, or data may contain secrets, credentials, tokens, or PII.
---

# secret-protection-review

Scan and report safe detection metadata without printing sensitive values. Block or redact secrets and record only safe handling evidence. This specialist review is conditional, not a default step for ordinary LOW-risk work; trigger it only at a secret boundary.

Return the scope, detection status, safe evidence reference, and unresolved handling decision. Never expose credentials or infer authorization.

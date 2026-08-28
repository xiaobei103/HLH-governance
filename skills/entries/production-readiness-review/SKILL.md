---
name: production-readiness-review
description: Use only for production, deployment, release, real users, or real customer data decisions.
---

# production-readiness-review

Review deployment, rollback, monitoring, secrets, data protection, disaster recovery, and persistent runtime evidence only when HIGH risk includes production or a formal release boundary.

Return `PASS`, `PASS WITH OBSERVATIONS`, `INCONCLUSIVE`, `FAIL`, or `NOT COMPLETED`. Tests, commits, or completion decisions cannot imply production readiness. Do not deploy, change production state, expose secrets, or grant the human release decision.

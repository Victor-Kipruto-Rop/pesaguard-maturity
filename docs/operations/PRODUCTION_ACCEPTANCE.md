# Production Replacement Acceptance Gates

The replacement must not receive production write traffic until all gates pass.

- [ ] API contracts used by current clients are mapped and compatibility-tested.
- [ ] Authentication, authorization and cross-tenant isolation tests pass.
- [ ] Database migrations are repeatable, reviewed and tested on a sanitized production-like copy.
- [ ] Financial invariants, idempotency and concurrent duplicate processing are tested.
- [ ] Daraja callback retries, duplicates, malformed payloads and provider outages are tested.
- [ ] Reconciliation outputs are deterministic and explainable; ambiguous matches are never silently accepted.
- [ ] Backups are restored successfully and recovery objectives are recorded.
- [ ] Security scans have no unresolved critical/high findings without a documented, approved exception.
- [ ] Load tests meet agreed latency and throughput targets with realistic data.
- [ ] Alerts, dashboards, incident runbooks and an on-call owner are available.
- [ ] Cutover plan, rollback trigger, rollback owner and communication plan are rehearsed.
- [ ] Only one backend is authorized to write live financial events at any time.
- [ ] A stabilization window and post-cutover verification checklist are agreed.

Record evidence and the approver for every item. A checked box without test output, runbook, or deployment evidence is not acceptance evidence.

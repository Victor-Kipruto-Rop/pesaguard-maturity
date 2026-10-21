# PesaGuard Maturity — Implementation Roadmap

## Operating constraints

- Keep the existing `api.pesaguard` production backend authoritative until the replacement passes acceptance gates and a controlled cutover.
- Do not run two independent writers against the same live financial events or tenant records.
- Treat this repository as a replacement candidate, not as production-ready because directories or manifests exist.
- Ship in small pull requests. Every phase must include tests, evidence, rollback notes and an updated status.
- Start as a modular monolith with separately scalable workers. Extract services only when measured operational needs justify it.

## Phase 0 — Secure and inventory

- [ ] Review `gateway/new.env`, all Git history and deployment logs for real credentials; revoke/rotate any exposed secrets.
- [ ] Remove local environment files, SQLite databases, virtual environments, caches, generated logs and machine-specific artifacts from Git.
- [ ] Add repository-wide ignore rules and secret scanning to CI.
- [ ] Inventory each service as `implemented`, `partial`, `scaffold`, or `not started`; do not infer status from directory existence.
- [ ] Make CI, CodeQL, dependency review, release and deployment workflows executable.
- [ ] Record known gaps, owners, acceptance tests and evidence links.

## Phase 1 — Runnable foundation

- [ ] Establish supported Python version, dependency locking, linting, formatting, typing and repeatable tests.
- [ ] Run the API gateway locally with health/readiness checks and strict configuration validation.
- [ ] Standardize structured logs, request IDs, error envelopes and secret-safe logging.
- [ ] Establish PostgreSQL migrations, connection pooling, tenant context and database health checks.
- [ ] Establish Redis/queue usage only where needed; define durable retry and dead-letter behavior.
- [ ] Define API versioning, OpenAPI contracts and compatibility tests.

## Phase 2 — Identity and tenant boundary

- [ ] Implement registration, email verification, login, refresh-token rotation, logout, password reset and session revocation.
- [ ] Use secure password hashing, generic authentication errors, rate limits and abuse protection.
- [ ] Implement users, organizations, memberships, roles, permissions and tenant-scoped authorization.
- [ ] Add MFA-ready architecture, audit events and administrative access controls.
- [ ] Use production PostgreSQL; SQLite may be used only in isolated tests if appropriate.

## Phase 3 — Financial core

- [ ] Implement immutable source transaction ingestion and idempotent event handling.
- [ ] Implement statement/file import with size limits, type validation, schema mapping and duplicate-file detection.
- [ ] Implement deterministic reconciliation with exact-match rules, ambiguity handling, exception queues and run history.
- [ ] Define financial decimal/currency rules, transaction state transitions and database constraints.
- [ ] Add audit history, safe corrections, replay tooling and data lineage.
- [ ] Prove tenant isolation and concurrency behavior with integration tests.

## Phase 4 — M-Pesa integration

- [ ] Implement only required and authorized Daraja APIs.
- [ ] Validate callback authenticity where provider capabilities support it, validate payloads, acknowledge safely and persist before asynchronous processing.
- [ ] Make duplicate callbacks safe through idempotency constraints.
- [ ] Cover timeout, retry, malformed payload, provider outage and replay scenarios.
- [ ] Never claim that callback ingestion initiates, confirms on behalf of the provider, refunds or settles payments.

## Phase 5 — Operational product capabilities

- [ ] Reconciliation exceptions and review workflows.
- [ ] Risk rules, explainable anomaly events and review outcomes.
- [ ] Reports and exports with tenant authorization and audit trails.
- [ ] Notifications, webhook signatures, delivery retries and delivery history.
- [ ] API keys, scopes, quotas, usage, developer documentation and sandbox support.
- [ ] Organization verification with configurable evidence and manual-review paths where authoritative automated checks are unavailable.

## Phase 6 — Reliability, security and operations

- [ ] Metrics, traces, structured logs, service-level objectives and actionable alerts.
- [ ] Automated backups and documented, tested restoration.
- [ ] Dependency, container, secret, SAST and dynamic security checks.
- [ ] Load, stress, concurrency, chaos and failure-recovery tests.
- [ ] Runbooks for provider outage, queue backlog, database saturation, credential compromise and failed migration.
- [ ] Define and test recovery time and recovery point objectives.

## Phase 7 — Migration and cutover

- [ ] Freeze and document API contracts currently consumed by `app.pesaguard.co.ke` and other clients.
- [ ] Map old models and endpoints to new contracts; write repeatable migration and reconciliation scripts.
- [ ] Test against a sanitized production-like data snapshot.
- [ ] Deploy the replacement to staging and run shadow comparisons without a second writer.
- [ ] Verify balances, counts, tenant boundaries, callbacks, reports, performance and recovery.
- [ ] Use a controlled traffic switch with a documented rollback trigger and owner.
- [ ] Keep the existing backend available for rollback until the agreed stabilization period ends.

## Definition of done

A capability is complete only when implementation, automated tests, API documentation, security/tenant checks, observability, operational instructions and deployment configuration exist and have been exercised. Placeholder files and passing import-only tests do not satisfy acceptance.

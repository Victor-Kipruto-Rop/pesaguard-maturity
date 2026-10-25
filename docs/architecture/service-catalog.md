# PesaGuard service catalogue and language ownership

Scope: Safaricom M-Pesa Daraja only. PesaGuard observes, normalizes, reconciles and reports on supported transaction data; it does not initiate, confirm, refund, transfer or settle funds.

## Java / Spring Boot
- `daraja-integration-service`: provider OAuth, API adapter, C2B/STK lifecycle, callback endpoints and provider normalization.
- `callback-ingestion-service`: durable callback receipt, evidence retention, deduplication and safe acknowledgement; initially may be a module in Daraja integration.
- `transaction-processing-service`: canonical transaction state machine, idempotency and event publication.
- `developer-api-gateway`: API-key verification, sandbox/production binding, quotas, request context and version routing.
- `webhook-delivery-service`: signed delivery, retries, history, replay, dead-letter handling and SSRF-safe URL validation.
- `audit-event-service`: append-only security/business audit events and retention controls.
- `integration-credentials-service`: preferably a managed-secret-manager integration for references, rotation metadata and audited access—not a custom vault.

## Python / FastAPI
- `reconciliation-service`: matching rules, run lifecycle, unmatched records, explainable decisions and exceptions.
- `data-quality-service`: schema, completeness, duplicate, consistency and freshness checks.
- `risk-service`: explainable risk signals and configurable rule versions; signals are not proof of fraud.
- `statement-import-service`: private uploads, file validation, scanning/quarantine integration, parsing and normalized ledger rows.
- `reporting-service`: tenant-scoped reports, exports and private artifacts.
- `analytics-service` (later): aggregate trends using governed, minimized datasets; not the source of truth for live transaction state.

## Elixir / Phoenix
- `platform-web`: customer app, LiveViews, dashboard and real-time updates.
- `organization-service`: organization profile, membership, onboarding state and tenant-scoped settings.
- `verification-orchestrator`: verification cases, evidence checklist and manual-review workflow. Registry/KRA/Peleza/GavaConnect checks must use verified contracts and real responses; otherwise report pending/manual review, never fabricate results.
- `developer-portal`: application/project management, sandbox onboarding, SDK/docs navigation and production-access requests.
- `notification-orchestrator`: preferences, in-app notifications and delivery coordination.
- `operations-status`: status presentation, incidents and maintenance notices; health must come from real checks.

## Shared infrastructure
PostgreSQL with service-owned schemas/roles; durable message broker; Redis-compatible cache for ephemeral state; private object storage; secrets manager/KMS; OpenTelemetry, metrics/logs/traces/alerts; CI, image registry and security scanning.

## Domain ownership rules
1. One authoritative owner for each write model: Java owns transaction lifecycle; Python owns reconciliation decisions; Elixir owns organization workflow state.
2. Cross-service reads/writes use authenticated APIs or versioned events, not shared-table writes.
3. Use inbox/outbox or equivalent durable delivery, idempotency keys and correlation IDs.
4. Separate sandbox and production API keys, provider credentials, callbacks and base URLs.
5. Tenant authorization applies in APIs, jobs, DB queries, cache keys, object storage and event consumers.
6. Start capabilities as modules; split into deployable services only when scale, ownership, risk or release cadence justifies it.

## Recommended initial deployable set
1. Phoenix platform (organization, onboarding, developer portal and status modules).
2. Java Daraja integration + callback ingestion.
3. Java transaction processing.
4. Java developer API gateway/key validation.
5. Java webhook delivery.
6. Python reconciliation.
7. Python data quality + risk modules, split later if justified.
8. Python statement import + reporting modules, split later if justified.
9. PostgreSQL, broker, cache, object storage and observability as managed infrastructure.

This target catalogue does not imply every listed service is implemented or production-ready.

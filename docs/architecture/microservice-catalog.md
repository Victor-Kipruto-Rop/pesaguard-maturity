# PesaGuard Microservice Catalog (Daraja-only)

## Architecture rule
This catalog is the target capability map, not a mandate to deploy every item as an independent process on day one. Start with bounded services; split only when deployment, scaling, security, ownership or reliability requires it. All services support M-Pesa Daraja only. PesaGuard observes/reconciles transaction evidence; it does not move money, initiate settlements, issue refunds or claim to confirm payment beyond authoritative provider evidence.

## Language allocation
- **Java / Spring Boot:** provider-facing and event delivery paths where strict contracts, mature JVM tooling and durable processing are useful.
- **Python / FastAPI:** data-heavy and analytical workloads: reconciliation, imports, quality, risk and reporting.
- **Elixir / Phoenix:** user workflows, developer platform, tenant administration, real-time dashboard and operational control surfaces.
- **Shared platform capabilities:** PostgreSQL, durable broker, object storage, secrets manager, OpenTelemetry, CI/CD. These are infrastructure capabilities, not automatically custom microservices.

## Java services
| Service | Responsibility | Priority |
|---|---|---|
| daraja-integration-service | OAuth token lifecycle, Daraja API adapter, environment isolation, provider request/response normalization | P0 |
| callback-ingestion-service | Receive callbacks, validate schema/size, persist immutable evidence, deduplicate and acknowledge safely | P0 |
| transaction-processing-service | Durable transaction lifecycle, explicit state transitions, inbox/outbox, recovery of unknown outcomes | P0 |
| webhook-delivery-service | Signed customer webhooks, bounded retries, delivery history, replay and dead-letter operations | P1 |
| provider-status-poller | Reconcile pending/unknown provider outcomes where the approved Daraja API supports it; rate-limit safely | P1 |
| api-edge-service | Optional gateway for routing, request limits and correlation IDs; do not duplicate identity/authorization carelessly | P2 |

## Python services
| Service | Responsibility | Priority |
|---|---|---|
| reconciliation-service | Match normalized Daraja records to tenant ledger/statement entries with versioned, explainable rules | P0 |
| statement-import-service | Secure file ingestion, scanning/quarantine, parsing and import lineage | P0 |
| data-quality-service | Completeness, duplicates, invalid fields, gaps and consistency findings | P1 |
| risk-service | Explainable anomaly/risk signals with rule version and evidence; never label a signal as proven fraud | P1 |
| reporting-service | Tenant-scoped reports, exports and audit of downloads | P1 |
| reconciliation-scheduler | Schedule recurring tenant jobs and prevent overlapping duplicate runs | P1 |
| analytics-aggregation-service | Precompute dashboard aggregates without exposing cross-tenant data | P2 |
| data-retention-worker | Policy-based retention/deletion workflows and verifiable audit trail | P2 |

## Elixir / Phoenix services
| Service | Responsibility | Priority |
|---|---|---|
| platform-web | Phoenix/LiveView user interface, dashboards, onboarding and operational views | P0 |
| identity-access-service | Authentication integration, sessions, MFA hooks, service identities and policy enforcement integration | P0 |
| tenant-organization-service | Organizations, memberships, roles, tenant configuration and onboarding state | P0 |
| developer-platform-service | Developer apps, sandbox credentials, API-key lifecycle, scopes, production-key requests | P1 |
| integration-configuration-service | Per-tenant Daraja configuration metadata, callback URLs and connection status; secrets stored in vault | P1 |
| audit-activity-service | Append-only security/admin audit events and authorized audit views | P1 |
| notification-service | In-app/email notification orchestration and user preferences; avoid duplicating provider webhook delivery | P2 |
| support-operations-service | Restricted support workflows, case records, audited time-bound access and break-glass approvals | P2 |
| status-page-service | Public service status and incident communication, backed by actual health/incident data | P2 |

## Shared platform capabilities (prefer managed products initially)
- PostgreSQL: service-owned schemas/roles, migrations, backups, restore drills and optional RLS defense-in-depth.
- Durable broker/queue: versioned events, retry budgets, dead-letter queues, replay and consumer lag alerts.
- Redis/Valkey: cache, rate-limit counters and ephemeral coordination only; never sole source of financial truth.
- Private object storage: uploaded statements, report artifacts and quarantined files; encryption and short-lived access links.
- Secrets/KMS: Daraja credentials, signing keys and rotation; never source-controlled.
- Observability: OpenTelemetry collector, metrics, logs, traces, dashboards and alerting.
- CI/CD and artifact registry: tests, SAST/dependency scans, signed immutable artifacts and environment approvals.

## Non-negotiable controls
1. Sandbox and production credentials, endpoints, API keys and callbacks are distinct.
2. Callbacks may be duplicate, delayed, reordered or missing. Persist evidence first; make consumers idempotent.
3. A timeout is an unknown outcome, not proof of failure. Preserve provider state separately from internal processing state.
4. Tenant authorization is enforced server-side at API, database, queue, cache, storage and export boundaries.
5. Use decimal-safe money representation, UTC timestamps, correlation IDs and redacted structured logs.
6. Every externally visible state and metric comes from real persisted/observed data, never fabricated progress or sample production data.
7. Use explicit retention, incident response, key rotation, backup/restore and disaster-recovery runbooks.

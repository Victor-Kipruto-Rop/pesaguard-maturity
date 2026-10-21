# Service Catalog and Ownership Boundaries

This catalog defines intended responsibilities, not claims that the corresponding directories are implemented. Update each row only after inspecting source code and test evidence.

| Domain / module | Owns | Required acceptance evidence | Initial deployment |
|---|---|---|---|
| API gateway | Routing, request IDs, edge limits, auth integration, error envelope | Gateway tests, abuse tests, route contract tests | Stateless API |
| Identity | Credentials, sessions, email verification, password reset | Auth flow tests, session revocation, security tests | Core API module |
| Tenancy and access | Organizations, memberships, roles, tenant authorization | Cross-tenant negative tests | Core API module |
| Integration adapters | Provider configuration and normalized provider events | Adapter contract tests and replay tests | Core API module / worker |
| M-Pesa ingestion | Supported Daraja callbacks and transaction ingestion | Duplicate, malformed, timeout and replay tests | Worker plus callback endpoint |
| Transactions | Canonical immutable source transaction records and state transitions | DB constraints, concurrency and idempotency tests | Core API module |
| Statement ingestion | Upload validation, parsing, mapping, import status and duplicate-file detection | Malformed-file and size-limit tests | Worker |
| Reconciliation | Deterministic matching, unmatched items, ambiguity and run history | Golden fixtures, invariants and repeatability tests | Core API module / worker |
| Risk and fraud | Rules, anomaly events, explanations and review status | Rule tests, audit tests, false-positive review tests | Core module initially |
| Reports and exports | Tenant-scoped summaries and export jobs | Permission, correctness and large-export tests | Core module / worker |
| Notifications | Email/SMS delivery orchestration and preferences | Retry, suppression and delivery-state tests | Worker |
| Webhooks | Signed outbound events, retry schedule and delivery history | Signature, replay and retry tests | Worker |
| API management | Keys, scopes, quotas, usage and revocation | Scope and quota enforcement tests | Core module |
| Audit | Append-only security and business audit events | Tamper/access tests and retention policy | Shared module |
| Configuration | Validated settings and safe feature flags | Invalid-config startup tests | Shared library |
| Health and telemetry | Liveness, readiness, metrics, traces and SLOs | Health dependency tests and alert checks | Shared infrastructure |
| Admin operations | Controlled support tools, failed-job review and access audit | Privilege tests and audit evidence | Core module |
| Developer experience | OpenAPI, examples, SDK generation and sandbox guidance | Spec validation and sample-client tests | Documentation / tooling |

## Deliberate exclusions from the initial live product

- Airtel Money and bank-provider integrations remain future work until separately implemented, tested and authorized.
- Payment initiation, money movement, refunds and settlement execution are outside the initial PesaGuard reconciliation scope.
- AI/ML fraud scoring is optional future capability. Begin with explainable deterministic rules and measurable outcomes.
- Billing/subscriptions, search clusters, service mesh, Kubernetes and a large fleet of microservices are not prerequisites for the first safe production release.

## Ownership rules

1. Each domain has one authoritative writer for its data.
2. Financial source records are immutable; corrections are new, auditable events.
3. Tenant identity must come from verified authentication context, never a client-supplied tenant ID alone.
4. Cross-domain work uses explicit contracts and idempotent commands/events.
5. Use a transactional outbox when database writes must reliably publish events.
6. Do not extract a domain into a network service until it has clear data ownership, contract tests, telemetry and an operational owner.

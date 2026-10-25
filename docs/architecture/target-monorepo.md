# PesaGuard target monorepo architecture

PesaGuard focuses on Safaricom M-Pesa Daraja ingestion, transaction monitoring, reconciliation, data quality, risk signals, reporting and developer integration. It does not originate, confirm, refund, move or settle funds.

- Java/Spring Boot: Daraja adapter, callback ingestion, durable provider evidence, transaction lifecycle and webhook delivery.
- Python/FastAPI: reconciliation, data quality, statement import, explainable risk rules and report generation.
- Elixir/Phoenix: customer platform, organization workflows, developer experience and real-time presentation.
- Shared: versioned API/event contracts, reference values, policies and sanitized fixtures.

Assume callbacks may duplicate, delay, reorder or go missing. Persist evidence durably; use database-backed idempotency, explicit state transitions and an outbox/inbox pattern or equivalent. Use decimal arithmetic for money. Enforce tenant isolation at APIs, workers, databases, cache, storage and event consumers. Sandbox and production credentials, keys, base URLs and callbacks must be separate. This scaffold is not proof of production readiness.

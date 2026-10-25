# PesaGuard — M-Pesa Daraja reconciliation infrastructure

PesaGuard is being rebuilt as an enterprise-grade platform focused on Safaricom M-Pesa Daraja. It ingests supported Daraja callbacks and reconciles transaction evidence against an organization's own ledger or imported records. It does **not** initiate, confirm, refund, move, or settle funds.

## Target language boundaries

- **Java / Spring Boot:** Daraja adapter and callback boundary, transaction lifecycle processing, signed webhook delivery.
- **Python / FastAPI:** reconciliation, data quality, statement import, explainable risk findings, reporting.
- **Elixir / Phoenix:** customer and developer platform, organization workflows, real-time presentation and background workflow coordination.
- **Shared resources:** versioned API/event contracts, reference data, security policies, sanitized fixtures, infrastructure and operations documentation.

## Repository map

- `apps/java/` — Java service modules and Gradle build.
- `apps/python/` — FastAPI service boundaries and Python tooling.
- `apps/elixir/` — Elixir umbrella applications; Phoenix web application needs generated endpoint/assets and full runtime wiring before deployment.
- `shared/contracts/` and `shared/schemas/` — initial API and event contracts.
- `infra/`, `deploy/`, `docs/`, `tests/` — infrastructure standards, operations guidance and readiness checklists.
- `compose.daraja.yml` — isolated local scaffold; does not replace the existing legacy Compose files.

## Local scaffold

Prerequisites: Docker Compose, Java 21/Gradle-compatible environment, Python 3.12, and Elixir/Erlang for the Phoenix workspace.

Start the isolated Java/Python scaffold and local dependencies:

```sh
docker compose -f compose.daraja.yml up --build
```

Local mapped ports are PostgreSQL `55432`, Redis `56379`, reconciliation liveness `18081`, Daraja integration `18082`, transaction processing `18083`, and webhook delivery `18084`. These services are foundations only; they do not yet implement the full production business workflows.

## Financial correctness and security requirements

- Treat callbacks as duplicate-able, delayed, reordered or missing. Persist evidence durably and use idempotent processing.
- A timeout or absent callback does not by itself prove a transaction failed.
- Use decimal arithmetic for monetary amounts and retain provider evidence.
- Enforce tenant authorization at every API, database, worker, cache, object-storage and event boundary.
- Keep sandbox and production credentials, keys, endpoints and callbacks separate.
- Never commit secrets, live customer data or unredacted production payloads.
- Treat risk signals as explainable findings, not proof of fraud.

## Readiness status

This repository contains scaffold code, service boundaries, contracts and operations guidance. It is **not yet production-ready**. Complete the checklist in `docs/operations/production-readiness-checklist.md`, implement durable storage and messaging, validate current approved Daraja flows, finish Phoenix runtime wiring, and pass integration, security, resilience and load tests before production use.

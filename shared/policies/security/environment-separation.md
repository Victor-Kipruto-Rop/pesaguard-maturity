# Sandbox and production separation

- Use separate Daraja credentials and configured provider endpoints for sandbox and production.
- Use separate PesaGuard API key namespaces, signing secrets, quotas and base URLs for sandbox and production.
- Reject sandbox keys on production routes and production keys on sandbox routes unless an explicitly documented policy permits otherwise.
- Never log secrets; reveal generated API secrets once and store only a verifier/digest where feasible.
- Record environment in requests, audit events, webhook configuration and telemetry.
- Test cross-environment rejection in CI and integration tests.

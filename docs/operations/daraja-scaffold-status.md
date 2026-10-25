# PesaGuard Daraja scaffold local run

This is a development scaffold, not production-ready fintech software. Existing `docker-compose.yml` is preserved.

Run the separate scaffold with `docker compose -f compose.daraja.yml up --build` only after reviewing it. The current Python reconciliation service exposes `/health/live`. Java services are framework shells and do not yet implement full Daraja callback persistence, durable messaging, or production authentication. Phoenix endpoint/router/assets must be generated before deployment. Use Daraja sandbox credentials only and never commit secrets.

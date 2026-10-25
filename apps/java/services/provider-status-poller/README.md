# Provider Status Poller (Java)
P1 recovery worker for pending/unknown transactions. Only call status/query operations supported by the approved Daraja product and merchant permissions. Apply rate limits, backoff, tenant/provider correlation, bounded polling windows and auditable operator replay. Never infer failure solely from a timeout or missing callback.

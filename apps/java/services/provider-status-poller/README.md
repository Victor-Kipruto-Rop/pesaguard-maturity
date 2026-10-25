# Provider Status Poller (Java)

P1 recovery worker for pending/unknown transactions. Call only status/query operations supported by the approved Daraja product and merchant permissions. Apply rate limits, backoff, bounded polling windows and auditable replay. A timeout or missing callback does not prove failure.

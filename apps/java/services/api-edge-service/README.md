# API Edge Service (Java, optional)

P2 optional gateway. Prefer a managed gateway until requirements justify owning this service. If implemented, add request-size limits, rate limits, correlation IDs, TLS policy and route allowlists. It must not replace service-level authorization, tenant checks, input validation or audit logging.

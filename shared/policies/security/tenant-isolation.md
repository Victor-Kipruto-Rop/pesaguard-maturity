# Tenant isolation requirements

- Resolve tenant identity from authenticated server-side claims or credential records; never trust a tenant ID supplied only in request JSON.
- Authorize every object access against the active tenant and actor permissions.
- Scope database queries, cache keys, object-storage paths, background jobs, events, exports and webhook delivery by tenant.
- Test cross-tenant reads/writes, identifier guessing and asynchronous job leakage.
- Use least-privilege service identities and database roles. Consider PostgreSQL row-level security as defense in depth, not as a substitute for application authorization.

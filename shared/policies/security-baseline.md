# Security baseline
- TLS in transit and encryption at rest for databases, object storage, backups and secrets.
- Least-privilege service identities; rotate provider and signing credentials.
- Enforce tenant access in each service and asynchronous worker.
- Validate webhook destinations against SSRF (loopback, private, link-local and cloud metadata ranges); revalidate DNS and redirects.
- Redact access tokens, consumer secrets, API keys, phone numbers and sensitive callback fields from logs.
- Rate-limit authentication, API-key operations, callbacks and expensive report endpoints.
- Verify backups with restore drills; protect audit trails against routine mutation.
- Maintain threat models, dependency scanning, incident response and access reviews.

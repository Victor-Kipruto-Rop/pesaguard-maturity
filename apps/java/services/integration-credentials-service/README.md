# Integration credentials service

**Language: Java / Spring Boot.** Prefer a managed secrets manager/KMS instead of storing raw secrets in this service. If needed, manage references, scope, rotation state and audited access—not UI access to credentials. Isolate Daraja sandbox and production credentials and use least-privilege service identities.

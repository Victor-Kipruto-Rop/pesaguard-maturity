# Callback ingestion service

**Language: Java / Spring Boot.** Receive supported Daraja callbacks, persist original payload and receipt metadata durably, deduplicate provider retries, validate expected shape, and acknowledge according to a tested durable-acceptance policy. Preserve provider evidence; redact sensitive values from logs. Initially may live inside `daraja-integration-service`.

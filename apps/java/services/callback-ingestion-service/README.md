# Callback Ingestion Service (Java)

P0 boundary for Daraja callback receipt. Validate request size and schema, persist immutable evidence, deduplicate durably, attach correlation IDs and commit before acknowledging. Handle repeated callbacks safely. Never log secrets or full sensitive payloads. Validate authenticity only with mechanisms actually supported by the configured Daraja product; do not invent signature headers. Hand work off via an outbox or durable queue.

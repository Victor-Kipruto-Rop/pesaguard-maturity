# Cross-service test strategy
Use unit tests for domain logic, integration tests for databases/brokers, contract tests for APIs/events, end-to-end tests for user journeys, and resilience/security/performance tests for release gates. Fixtures must be synthetic or sanitized. Never load-test live Daraja production endpoints without explicit authorization.

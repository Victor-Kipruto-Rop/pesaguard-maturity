# Service ownership register

| Capability | Owner | Boundary |
|---|---|---|
| Daraja OAuth/provider adapter | Java Daraja Integration | Provider secrets restricted to this service. |
| Callback evidence and normalization | Java integration/transaction boundary | Durable persistence and deduplication. |
| Normalized transaction lifecycle | Java Transaction Processing | State transitions and durable events. |
| Reconciliation runs, matches, exceptions | Python Reconciliation | Deterministic, explainable, versioned rules. |
| Data quality findings | Python Data Quality | Preserve source evidence. |
| Statement parsing/import | Python Statement Import | Private storage, scanning and validation. |
| Risk findings | Python Risk | Explainable signals, not proof of fraud. |
| Report generation | Python Reporting | Tenant-scoped queries and private artifacts. |
| User workflows/dashboard | Elixir/Phoenix | UI is not the authorization boundary. |
| Webhook delivery attempts | Java Webhook Delivery | Signing, retries, SSRF controls and replay. |
| Shared API/event contracts | Shared resources | Compatibility checks in CI. |

# Event catalog (initial draft)

All event contracts must be versioned and validated in CI before production use. Include event_id, event_type, schema_version, occurred_at, correlation_id, producer and tenant reference where appropriate. Never include secrets or unnecessary personal data.

- daraja.callback.received.v1
- daraja.callback.rejected.v1
- transaction.normalized.v1
- transaction.state_changed.v1
- transaction.outcome_unknown.v1
- reconciliation.run_requested.v1
- reconciliation.run_completed.v1
- reconciliation.exception_created.v1
- reconciliation.exception_resolved.v1
- data_quality.finding_created.v1
- risk.signal_created.v1
- report.generated.v1
- webhook.delivery_attempted.v1
- webhook.delivery_failed.v1
- organization.verification_state_changed.v1
- developer.production_key_requested.v1
- security.audit_event_recorded.v1

The names are proposed contracts, not proof that publishers or consumers exist yet.

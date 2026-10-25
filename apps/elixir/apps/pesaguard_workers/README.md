# Background workers
Use Oban/PostgreSQL-backed jobs for retryable orchestration and notifications. Every job must be idempotent, bounded by retry policy, observable, and safe for tenant-scoped data.

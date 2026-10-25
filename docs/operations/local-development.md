# Local development

The new Daraja services are separated from the existing legacy Compose stack. Use only Daraja sandbox credentials. Never commit provider credentials or customer data. The Java services currently provide framework foundations, not complete provider callback or persistence workflows. The Phoenix application needs generated endpoint/router/assets before it can be deployed. Validate every service with tests and dependency checks before using it beyond local development.

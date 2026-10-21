# Secret Exposure Response Checklist

Use this checklist if a real credential, signing key, token, or private configuration is committed.

1. Identify the credential owner and systems that trust it.
2. Revoke or rotate it immediately; do not wait for history cleanup.
3. Review access logs for use since the earliest known exposure.
4. Remove the value from the working tree and Git history where practical.
5. Coordinate history rewrites with contributors before force-pushing; never assume history rewriting invalidates a credential.
6. Replace committed values with placeholders and document required secret names.
7. Store production values in the deployment platform's secret manager.
8. Add secret scanning to pull requests and default-branch pushes.
9. Record impact, remediation, and verification without copying the secret into tickets or logs.

Removing a file from a branch does not invalidate a secret and does not erase earlier Git commits.

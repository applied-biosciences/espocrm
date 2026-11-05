# Stage 19 Production Readiness

Stage 19 prepares NuriVoyage for the separately approved AWS production release. The local stack is the release rehearsal environment; it does not deploy to AWS or contain production credentials.

## Readiness controls

- Docker images are pinned by digest and local services expose loopback ports by default.
- `scripts/local production-check` verifies required environment secret names, loopback binding, pinned images and service health.
- `scripts/local backup` creates a database dump, object archive and SHA-256 manifest.
- `scripts/local restore BACKUP_DIR` restores the database and object storage for a disaster-recovery rehearsal.
- Health endpoints cover MariaDB, CRM, daemon, WebSocket, MinIO, Mailpit and the application shell.
- `NvProductionReadiness` records infrastructure, monitoring, backup, disaster-recovery, secrets and release-gate evidence.

## Release gate

Run `scripts/local production-check`, `scripts/local smoke-stage19`, and `scripts/local smoke`. Review the generated backup manifest and restore result. An AWS release still requires a separately approved account, network, managed database/object storage, secret manager, monitoring and rollback plan.

## AWS handoff checklist

1. Create or select the production AWS account and region and record them in the release ticket.
2. Provision private networking, HTTPS termination, a managed MariaDB-compatible database, private versioned S3 storage, secrets management, centralized logs and metrics.
3. Supply site URL, WebSocket URL, database, SMTP and S3 settings through the secrets manager. Never copy `.env` or local MinIO credentials into AWS.
4. Deploy the pinned EspoCRM image and custom release artifact through the approved CI/CD role.
5. Run migration, metadata rebuild, health checks, the end-to-end booking smoke test and a backup/restore rehearsal in the release environment.
6. Enable monitoring, alerts, database backups, object versioning and retention before opening traffic.
7. Record rollback image, restore point, DNS cutover and incident contacts. Promote only after sign-off.

This repository does not contain AWS account IDs, private keys, Terraform state, production secret values or an AWS apply command.

## End-to-end client booking journey

The Stage 19 smoke test creates synthetic records for customer, enquiry, accepted quote, confirmed booking, lead traveller, invoice and deposit payment. It verifies the key relationships and leaves the local services running for human UAT.

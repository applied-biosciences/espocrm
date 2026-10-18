# Stage 19 Production Readiness

Stage 19 prepares NuriVoyage for a separately approved production release. The local stack is the release rehearsal environment; it does not deploy to AWS or contain production credentials.

## Readiness controls

- Docker images are pinned by digest and local services expose loopback ports by default.
- `scripts/local production-check` verifies required environment secret names, loopback binding, pinned images and service health.
- `scripts/local backup` creates a database dump, object archive and SHA-256 manifest.
- `scripts/local restore BACKUP_DIR` restores the database and object storage for a disaster-recovery rehearsal.
- Health endpoints cover MariaDB, CRM, daemon, WebSocket, MinIO, Mailpit and the application shell.
- `NvProductionReadiness` records infrastructure, monitoring, backup, disaster-recovery, secrets and release-gate evidence.

## Release gate

Run `scripts/local production-check`, `scripts/local smoke-stage19`, and `scripts/local smoke`. Review the generated backup manifest and restore result. An AWS release still requires a separately approved account, network, managed database/object storage, secret manager, monitoring and rollback plan.

## End-to-end client booking journey

The Stage 19 smoke test creates synthetic records for customer, enquiry, accepted quote, confirmed booking, lead traveller, invoice and deposit payment. It verifies the key relationships and leaves the local services running for human UAT.

# Stage 2 automated localhost smoke test

Run UTC: 2026-10-16T21:42:23.394269+00:00

Command: `scripts/local smoke` from the branch root.

This executes Docker Compose startup and health checks, authenticated API requests, stack/MinIO restarts, an offline backup and destructive change/restore of synthetic test records. Uses local `.env` credentials without printing them.

| Check | Result | Evidence |
|---|---|---|
| 01 Compose startup | PASS | docker compose up -d --wait succeeded |
| 02 Container health | PASS | PASS db: running/healthy PASS crm: running/healthy PASS daemon: running/healthy PASS websocket: running/healthy PASS minio: running/healthy PASS mailpit: running/healthy PASS http://localhost:8080/ PASS http://localhost:9000/minio/health/live PASS http://localhost:8025/readyz |
| 03 Local login page | PASS | HTTP 200; EspoCRM application shell |
| 04 Administrator authentication | PASS | admin |
| 05 MariaDB | PASS | Connection and InnoDB healthy |
| 06 Create customer/contact | PASS | Account 6ad299ccf372ce19e; Contact 6ad299cd2fc850eb6 |
| 07 Stack restart and record persistence | PASS | Smoke Customer 1a5f3aaef3 |
| 08 Authorised MinIO document path | PASS | MinIO object exists; authenticated admin/Operations download matches bytes; anonymous/Sales denied |
| 09 MinIO persistence | PASS | Object survives MinIO restart and authorised download matches bytes |
| 10 Espo email to Mailpit | PASS | Espo Email 6ad299f373899d33b delivered to Mailpit: NuriVoyage Smoke 1a5f3aaef3 |
| 11 Daemon and scheduler | PASS | 19 scheduled jobs; at least one lastRun set; no daemon fatal errors |
| 12 WebSocket | PASS | HTTP 101 WebSocket upgrade |
| 13 Backup validity | PASS | backups/20261016T214108631916Z; SQL and runtime/object archive validated with SHA-256 manifest |
| 14 Restore recovery and object deletion | PASS | Changed customer and deleted MinIO object recovered with matching bytes; contact relationship retained |
| 15 Final service health | PASS | PASS db: running/healthy PASS crm: running/healthy PASS daemon: running/healthy PASS websocket: running/healthy PASS minio: running/healthy PASS mailpit: running/healthy PASS http://localhost:8080/ PASS http://localhost:9000/minio/health/live PASS http://localhost:8025/readyz |
| 16 Organisation defaults | PASS | ZAR reporting/base; ZAR/USD/GBP/EUR/SAR/AED; DD/MM/YYYY |
| 17 Role boundaries | PASS | Seven role personas authenticated; API cost read/write denials, commercial access, hybrid sales/ops modules and own-only commissions verified |
| 18 Role write paths | PASS | Sales customer create/edit succeeds; agent commission creation denied; Operations traveller/customer link succeeds and customer edit denied; all 19 modules readable by Management |

Human UAT remains **PENDING**. See [exact human checklist](stage-2-human-uat.md).

Implementation scope and limitations: [Stage 1 design](../nurivoyage/stage-1-design.md). No AWS deployment or production data used.

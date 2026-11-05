# Stage 1–2 local handoff

## Environment

Local CRM: http://localhost:8080. Mailpit: http://localhost:8025. MinIO console: http://localhost:9001. WebSocket: ws://localhost:8081. Six persistent services run in the `nurivoyage` Compose project; a one-shot private-bucket initializer exits successfully. The stack is left running for human testing. No AWS resources were deployed and no production data was used.

Repository branch: `codex/nurivoyage-stage-1-2`. Initial task commit: `b8081f0f3742642da8388082e3e7f745aa94592a`. Implementation commit is available from `git log -1`; no master commit or merge is performed by this task.

## Credentials and UAT

Run `scripts/local credentials` and open `.local/test-credentials.md` for exact local test passwords. Admin role login: `admin@nuri.local`. All seven usernames and reset steps are in [the exact 20-step human UAT checklist](stage-2-human-uat.md). Credentials and the private sheet are ignored by Git. Human acceptance is **PENDING** until a human performs and signs that checklist.

## Validation evidence

- A clean reset/start created and configured the full stack successfully with all six services healthy.
- A separate fresh Git-index checkout successfully generated its own random `.env`, retained executable scripts and all custom controllers/metadata, and passed `docker compose config -q`.
- Browser inspection confirmed the NuriVoyage page title, Username/Password fields, Log in button and retained EspoCRM legal notice.
- [Automated smoke report](stage-2-smoke-test.md) records the final full run and exact evidence. Reproduce using `scripts/local smoke`.
- Custom JSON resources, shell syntax, Python syntax and custom PHP syntax validated; `git diff --check` passed.
- Staged-file scan confirmed local generated passwords, `.env`, `.local`, runtime data and backups are absent from the commit.

## Known limitations and intended later scope

- Human UAT and optional phone/tablet LAN testing have not been completed. Ports bind to localhost by default; temporary LAN instructions are in the checklist.
- Workflows are manual status baselines. Automatic approvals/PO emailing, deposit reconciliation, live FX, calculated balances/debtors/creditors, profitability dashboards and immutable historical commission posting are future implementation described in [Stage 1 design](../nurivoyage/stage-1-design.md).
- Espo technical administrators inherently bypass commercial ACL. Use the Management account for daily commercial work and admin only for system maintenance.
- MinIO is built from the pinned upstream community source commit because former upstream registry/download endpoints were unavailable. The first build requires internet. The standard S3 storage interface is preserved. Production storage/provider/security selection belongs to a future stage.
- The environment runs the official EspoCRM 10.0.10 distribution matching this fork's version, with this branch's supported custom directories mounted. Core development/frontend rebuilds are not needed for this stage.
- Backup/restore is a local schema-v1 snapshot workflow requiring the matching checkout and original `.env`. It restores MariaDB, runtime data, MinIO and Mailpit; it does not roll back Git source. It causes brief local downtime and must not run concurrently with bootstrap or smoke tests.

The generated purchaseCostConverted field is explicitly denied alongside the original cost/currency for restricted roles, and targeted tests verify that Sales can create/edit customers and Operations can create linked travellers without editing customers. The stale removed-document URL error was fixed with a custom S3 adapter subclass, without editing Espo core. Other operational storage errors retain their original error behavior.

## Changed files

[Complete changed-file manifest](stage-2-changed-files.md). Main areas: Compose and pinned MinIO build; custom entities/controllers/layouts/translations and storage adapter; bootstrap/seed/role scripts; local lifecycle and snapshot helpers; end-to-end tests; Stage 1 design/migration notes; smoke/UAT reports; README and repository guidance.

# Schema migrations

## v1 — Stage 1–2 initial local foundation

`model.json` declares schemaVersion=1 and Espo version 10.0.10. Supported JSON entity definitions create 19 Nv entities and their belongs-to relationships. `php rebuild.php` uses Espo's schema tool; no core SQL patch is applied. Native Account, Contact and Lead are reused. A metadata-registered S3 adapter subclass maps confirmed missing files to HTTP 404; no core storage code changes. All metadata/layouts/translations are tracked under custom/Espo/Custom/Resources.

Initial order: Compose installs core and schema → `bootstrap.php` checks version, configures defaults/storage/mail, upserts roles/users, seeds synthetic data once → rebuild → restart worker/websocket. `nurivoyageSeedVersion` prevents re-seeding after users edit records. Bootstrap preserves existing user passwords unless explicitly passed `--reset-passwords`; role grants are reconciled every time. Config defaults are reconciled from `.env`/bootstrap.

Before future schema changes: take `scripts/local backup`, add a numbered migration note with affected fields and preservation strategy, update the manifest version and compatibility checks, rebuild, run smoke/role tests, then commit. Backups are schema-v1 snapshots and restore with this checkout and its original `.env`; they do not roll back Git/customisation code. Never restore a v1 DB into a changed schema without a reviewed migration plan. `scripts/local reset-local` is the explicit destructive fresh-install path and requires a typed confirmation. `scripts/local stop` preserves volumes.

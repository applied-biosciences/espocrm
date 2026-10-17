# Schema migrations

## v1 — Stage 1–2 initial local foundation

`model.json` declares schemaVersion=1 and Espo version 10.0.10. Supported JSON entity definitions create 19 Nv entities and their belongs-to relationships. `php rebuild.php` uses Espo's schema tool; no core SQL patch is applied. Native Account, Contact and Lead are reused. A metadata-registered S3 adapter subclass maps confirmed missing files to HTTP 404; no core storage code changes. All metadata/layouts/translations are tracked under custom/Espo/Custom/Resources.

Initial order: Compose installs core and schema → `bootstrap.php` checks version, configures defaults/storage/mail, upserts roles/users, seeds synthetic data once → rebuild → restart worker/websocket. `nurivoyageSeedVersion` prevents re-seeding after users edit records. Bootstrap preserves existing user passwords unless explicitly passed `--reset-passwords`; role grants are reconciled every time. Config defaults are reconciled from `.env`/bootstrap.

Before future schema changes: take `scripts/local backup`, add a numbered migration note with affected fields and preservation strategy, update the manifest version and compatibility checks, rebuild, run smoke/role tests, then commit. Backups are schema-v1 snapshots and restore with this checkout and its original `.env`; they do not roll back Git/customisation code. Never restore a v1 DB into a changed schema without a reviewed migration plan. `scripts/local reset-local` is the explicit destructive fresh-install path and requires a typed confirmation. `scripts/local stop` preserves volumes.

## Stage 3 — no schema version change

Stage 3 adds a supported theme, login/navbar views, grouped tab configuration, labels/icons, main detail-layout polish and three native EmailTemplate records. It retains schemaVersion=1 and the existing business entities, fields and financial ACL. Management is granted the existing EmailTemplate scope to review templates; restricted-role cost/commission grants remain unchanged. No SQL migration or core upgrade is performed. Reapply via `scripts/local bootstrap`; original assets and generated publication copies are versioned. Human Stage 2 acceptance is recorded separately from the new Stage 3 UAT.

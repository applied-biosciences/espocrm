# Schema migrations

## v1 — Stage 1–2 initial local foundation

`model.json` declares schemaVersion=1 and Espo version 10.0.10. Supported JSON entity definitions create 19 Nv entities and their belongs-to relationships. `php rebuild.php` uses Espo's schema tool; no core SQL patch is applied. Native Account, Contact and Lead are reused. A metadata-registered S3 adapter subclass maps confirmed missing files to HTTP 404; no core storage code changes. All metadata/layouts/translations are tracked under custom/Espo/Custom/Resources.

Initial order: Compose installs core and schema → `bootstrap.php` checks version, configures defaults/storage/mail, upserts roles/users, seeds synthetic data once → rebuild → restart worker/websocket. `nurivoyageSeedVersion` prevents re-seeding after users edit records. Bootstrap preserves existing user passwords unless explicitly passed `--reset-passwords`; role grants are reconciled every time. Config defaults are reconciled from `.env`/bootstrap.

Before future schema changes: take `scripts/local backup`, add a numbered migration note with affected fields and preservation strategy, update the manifest version and compatibility checks, rebuild, run smoke/role tests, then commit. Backups are schema-v1 snapshots and restore with this checkout and its original `.env`; they do not roll back Git/customisation code. Never restore a v1 DB into a changed schema without a reviewed migration plan. `scripts/local reset-local` is the explicit destructive fresh-install path and requires a typed confirmation. `scripts/local stop` preserves volumes.

## Stage 3 — no schema version change

Stage 3 adds a supported theme, login/navbar views, grouped tab configuration, labels/icons, main detail-layout polish and three native EmailTemplate records. It retains schemaVersion=1 and the existing business entities, fields and financial ACL. Management is granted the existing EmailTemplate scope to review templates; restricted-role cost/commission grants remain unchanged. No SQL migration or core upgrade is performed. Reapply via `scripts/local bootstrap`; original assets and generated publication copies are versioned. Human Stage 2 acceptance is recorded separately from the new Stage 3 UAT.

## Stage 4 — enquiry workflow extension

Stage 4 adds operational lead and enquiry fields to the existing `NvEnquiry` entity: contact, source, source detail, destination, service type, preferred contact method, budget, next follow-up and lost reason. This is an additive metadata change applied by `scripts/local bootstrap`; no core files, SQL migration or external integration is introduced. Existing Stage 1 status vocabulary and role boundaries remain in force.

## Stage 5 — traveller and document metadata

Stage 5 adds passport identity metadata to `NvTraveller` and document number, issuing country, issue date and verification state to `NvTravelDocument`, including read-only verification attribution. This is an additive metadata change applied by `scripts/local bootstrap`; files remain in the existing private MinIO-backed document path and no OCR, external identity validation or AWS deployment is introduced.

## Stage 6 — quote and version metadata

Stage 6 adds quote number, option name, sent-at, accepted-at and lost-reason fields to `NvQuote`. It also publishes the application version marker `v10.0.10.0` through supported custom login, navbar and client head assets. This is an additive metadata and presentation change; the EspoCRM distribution remains pinned to 10.0.10 and no core files are changed.

## Stage 7 — traveller passport photo

Stage 7 adds a private `passportPhoto` file field to `NvTraveller`, adds itinerary metadata to `NvBooking`, and publishes the application version marker `v10.0.10.0.s7` through supported login, navbar and client head assets. Traveller records and their photos are readable by all named application roles, including Sales; the separate travel-document module remains role-protected. Photos use the existing authenticated attachment storage path; no public image URL, OCR or face recognition is introduced.

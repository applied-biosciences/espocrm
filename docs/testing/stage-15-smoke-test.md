# Stage 15 repair smoke test — 17 October 2026

Version: `v10.0.10.0.s15`

- `scripts/local bootstrap`: PASS, exit 0 (repeated after full restore).
- `scripts/local smoke`: all 18 checks PASS, including stack restart, MinIO access, Mailpit delivery, backup/restore and seven-role boundaries.
- `scripts/local smoke-stage15`: PASS browser controller registration and authenticated API list access for Tax Rules, Conversion Snapshots and Customer Communications (admin, finance, manager, sales); one deployed FX navigation item; live Frankfurter v2 rates and all 16 currency pairs.
- `node tests/nurivoyage/fx-converter.cjs`: PASS actual view calculations from every input, refresh preservation and provider error handling.
- `scripts/local smoke-stage11`: PASS commission lifecycle regression.
- Browser: Tax Rules, Conversion Snapshots and Customer Communications lists load without 404. Empty lists correctly display No Data.
- Browser converter: input from ZAR, USD, GBP and SAR updates all other fields. Update rates succeeds and preserves selected source amount. USD 100 produced GBP 75.22, ZAR 1,645.76 and SAR 375.00 at the provider rates observed during testing. These are test evidence, not fixed rates.

The first baseline attempt was interrupted by editing the launcher during its restore subprocess. The clean rerun above completed successfully. Browser calculator does not change transaction snapshots or accounting defaults. Human UAT remains with the user.

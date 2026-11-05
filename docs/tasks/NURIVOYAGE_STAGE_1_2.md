# NuriVoyage Stage 1–2 Development Task

## Objective
Build the local foundation for **NuriVoyage**, the white-labelled travel management platform for **Nuri's Travel**, using this EspoCRM fork.

Complete Stage 1 and Stage 2 locally before any AWS work.

Development branch: `codex/nurivoyage-stage-1-2`

Do not commit Stage 1–2 work directly to `master`.

---

# Stage 1 — Core business model

## Organisation defaults
- Product name: **NuriVoyage**
- Company: **Nuri's Travel**
- Base/reporting currency: **ZAR**
- Enable: ZAR, USD, GBP, EUR, SAR, AED
- Date format: DD/MM/YYYY
- Timezone configurable

## Initial roles
Create these roles:
1. Sales Agent
2. Operations
3. Sales + Operations Hybrid
4. Sales + Operations Commercial
5. Finance
6. Management
7. System Administrator

### Sales Agent
Can access leads/enquiries, customers, quotes, bookings, customer balances/payments and own commission.

Must not access supplier purchase costs, supplier invoices, gross profit, company margin, other agents' commissions or creditor reporting.

### Operations
Can access bookings, travellers, flights, hotels, transfers, visas, travel documents and supplier confirmations.

Do not grant full profitability visibility by default.

### Sales + Operations Hybrid
Combines Sales Agent and Operations access.

Must not automatically see supplier purchase costs, total booking gross profit, company margin, other agents' commissions or management dashboards.

### Sales + Operations Commercial
Same as Hybrid, plus supplier prices/costs required to complete operational bookings.

Must still not see overall booking gross profit, company-wide margin, other agents' commissions, full creditor position or management-only reporting by default.

### Finance
Can access customer invoices/payments, purchase orders, supplier bills/payments, debtors, creditors, FX data and commission payment status.

### Management
Full commercial visibility including sales, supplier costs, gross profit, gross margin, net contribution, commissions, debtors and creditors.

### System Administrator
Technical and system administration. Keep technical administration separate from commercial access where practical.

## Core entities
Use native Espo entities where suitable. Create custom entities only where required.

Prepare these entities and relationships:
- Account / Customer
- Contact
- Lead
- Enquiry
- Traveller
- Quote
- Booking
- Booking Item
- Supplier
- Purchase Order
- Supplier Bill
- Customer Invoice
- Customer Payment
- Supplier Payment
- Commission
- FX Rate
- Travel Document
- Hotel
- Flight
- Transfer
- Visa
- Package

## Sales workflow baseline
New Enquiry → Qualified → Quote Prepared → Quote Sent → Follow-up → Customer Accepted → Deposit Requested → Deposit Paid → Booking Confirmed

Terminal states:
- Lost
- Cancelled
- Expired Quote

## Supplier workflow baseline
Booking Confirmed → Supplier Selected → Purchase Order Created → PO Emailed → Supplier Confirmation → Supplier Invoice Received → Payment Due → Paid

## Profitability model
Document for later implementation:

Selling Price
- Flight Cost
- Hotel Cost
- Transfer Cost
- Visa Cost
- Insurance Cost
- Other Direct Costs
= Gross Profit

Gross Profit
- Sales Agent Commission
= Net Contribution

Sales Agent and standard Hybrid users must not see this model.

## Commission model
Document support for:
- % of sale
- % of gross profit
- fixed amount
- product-specific commission

Historical commission values must later be frozen so changes to commission rules do not alter previous bookings.

Create a Stage 1 design document under `docs/nurivoyage/` describing entities, relationships, workflows and permission boundaries.

---

# Stage 2 — Local development environment

Build a fully reproducible local NuriVoyage environment with **no AWS dependency**.

## Docker Compose stack
At minimum include:
- EspoCRM application
- MariaDB
- Espo daemon/worker
- Espo websocket service if required by the installed version
- MinIO for local S3-compatible document storage
- Mailpit for local SMTP/email testing

Use pinned container versions. Do not leave production-ready configuration on unpinned `latest` tags.

Target URL:
- `http://localhost:8080`

Optional local alias:
- `http://nurivoyage.local`

## Customisation structure
Keep NuriVoyage changes separate from EspoCRM core. Follow supported Espo extension/customisation paths for this version.

Prepare or use:
- `custom/`
- `client/custom/`
- `branding/`
- `scripts/`
- `tests/`
- `infrastructure/terraform/`

Avoid core edits. If a core edit is unavoidable, document the exact reason and upgrade impact.

## Environment configuration
Add `.env.example` with placeholders only.

Make sure `.env` is ignored.

Include placeholders for:
- Espo admin user/password
- DB name/user/password/root password
- MinIO access key/secret
- SMTP host/port
- application URL
- `DEFAULT_CURRENCY=ZAR`

Do not commit real secrets.

## Persistence
Persist:
- MariaDB data
- Espo data/custom paths required by this version
- MinIO data

`docker compose down` must preserve data.

Only an explicit reset action may destroy local development data.

## MinIO proof
Use MinIO for synthetic travel documents.

Prove locally:
- upload synthetic PDF/image
- retrieve it through the intended authorised application path
- delete it
- confirm persistence across restart

Do not use real passport/customer data.

Keep storage abstraction compatible with later AWS S3 use.

## Mailpit proof
Route all local outbound mail to Mailpit.

Prove EspoCRM can send a test email and that it appears in Mailpit.

Do not send real customer/supplier email.

## Development users
Create or document reproducible setup for synthetic users:
- `admin@nuri.local`
- `manager@nuri.local`
- `finance@nuri.local`
- `sales@nuri.local`
- `operations@nuri.local`
- `hybrid@nuri.local`
- `hybrid-commercial@nuri.local`

Do not commit real passwords. Provide a reset/bootstrap method.

## Seed data
Create synthetic development data only.

Customers:
- Ahmed Khan
- Fatima Patel
- Mohammed Ismail

Suppliers:
- Demo Airways
- Demo Makkah Hotel
- Demo Madinah Hotel
- Demo Transfers
- Demo Visa Services

Example scenarios:
- Umrah Family Package
- Dubai Holiday
- Cape Town → London flight

Use mixed currencies such as:
- ZAR sale
- USD hotel
- USD flight
- SAR ground service

## Helper scripts
Provide scripts or equivalent documented commands for:
- start
- stop
- backup
- restore
- reset-local
- health-check

Reset must warn before deleting local data.

Backup/restore must cover MariaDB and, where practical, MinIO test data.

## Logging
Document how to inspect:
- Espo application logs
- PHP/application errors
- MariaDB errors
- daemon/scheduler errors
- websocket errors
- MinIO errors
- Mailpit/email problems

`docker compose logs -f` should give useful output.

## Codex development rules
Add repository guidance stating:
1. Do not edit EspoCRM core unless unavoidable.
2. Use supported custom directories/extensions.
3. Never commit credentials.
4. Never use production customer data locally.
5. Run tests before committing.
6. Do not silently upgrade EspoCRM or MariaDB.
7. Preserve and document schema migrations.
8. Document custom entities and fields.
9. Keep AWS infrastructure separate from application business logic.
10. Keep document storage compatible with MinIO locally and AWS S3 later.

---

# Automated localhost smoke test

After implementation, run a fresh local smoke test from this branch.

Required checks:
1. `docker compose up -d` succeeds.
2. Required containers are healthy/running.
3. `http://localhost:8080` loads the NuriVoyage/Espo login page.
4. Admin login works.
5. MariaDB connection is healthy.
6. Create a synthetic customer/contact.
7. Restart the stack and confirm the record persists.
8. Upload a synthetic document to MinIO.
9. Restart MinIO and confirm the object persists.
10. Send a test Espo email and confirm it appears in Mailpit.
11. Espo daemon/scheduled jobs run without fatal errors.
12. Websocket service passes a basic check if used.
13. Backup script creates a valid backup.
14. Delete/change a synthetic record, restore, and confirm recovery.
15. Run health-check and report PASS/FAIL per service.

Create:
- `docs/testing/stage-2-smoke-test.md`

Include exact commands and results.

Do not mark complete while any required check fails.

---

# Human localhost acceptance test

After automated smoke testing passes, leave the environment running for manual testing.

Create:
- `docs/testing/stage-2-human-uat.md`

The checklist must include exact local URLs and the development credential/reset method.

Human tester verifies:
1. Open `http://localhost:8080`.
2. Login page loads.
3. Login as System Administrator.
4. Login as Sales Agent.
5. Login as Operations.
6. Login as Sales + Operations Hybrid.
7. Login as Sales + Operations Commercial.
8. Login as Finance.
9. Login as Management.
10. Each role sees the intended modules/navigation.
11. Sales cannot access management profitability or restricted supplier-cost data.
12. Hybrid receives both sales and operations access.
13. Hybrid Commercial can access required supplier-cost information but not full management access.
14. Create/edit a synthetic customer.
15. Confirm ZAR is base currency and USD/GBP/EUR/SAR/AED are available.
16. Upload/retrieve a synthetic document.
17. Send a test email and inspect it in Mailpit.
18. Test responsive layout from phone/tablet on the same LAN if practical.
19. Restart Docker and confirm records/documents persist.
20. Record UI, permission or workflow defects.

Do not treat manual UAT as passed until a human has completed the checklist.

---

# Deliverables

The branch must contain:
- working Docker Compose local environment
- pinned service versions
- `.env.example`
- `.gitignore` protection for secrets/local data
- Stage 1 NuriVoyage data-model and workflow documentation
- initial roles and permission model
- synthetic users/seed-data setup
- MinIO local document-storage proof
- Mailpit local email proof
- backup/restore tooling
- reset tooling
- health-check tooling
- automated localhost smoke-test report
- human localhost UAT checklist
- README instructions to clone, configure, start, stop and test

## Definition of done
Stage 1–2 is complete only when:
- a fresh checkout can be configured from documentation
- full stack starts with Docker Compose
- localhost login works
- persistence works
- MinIO works
- Mailpit works
- roles exist and basic access boundaries are verified
- ZAR and required currencies are configured
- backup and restore are proven
- automated localhost smoke test passes
- human localhost UAT checklist is ready and environment can be tested manually
- no AWS deployment has occurred
- no production/customer data is used

When complete, commit all work to `codex/nurivoyage-stage-1-2` and open a pull request against `master` containing smoke-test results and known limitations.
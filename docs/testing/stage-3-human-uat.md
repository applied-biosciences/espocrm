# Stage 3 human localhost acceptance

Status: **PENDING**. Stage 2 was accepted by the user on 17 October 2026. That approval does not mark this new Stage 3 build accepted. Choose PASS / FAIL / CHANGE REQUESTED for every test; record notes and sign below. Do not merge Stage 3 before explicit human acceptance.

## Local access

- CRM: http://localhost:8080
- Mailpit: http://localhost:8025
- MinIO console (optional storage review): http://localhost:9001
- Quote layout: http://localhost:8080/client/custom/branding/pdf/quotation.html
- Invoice layout: http://localhost:8080/client/custom/branding/pdf/invoice.html
- PO layout: http://localhost:8080/client/custom/branding/pdf/purchase-order.html
- Branch: `codex/nurivoyage-stage-3`, based on approved Stage 1–2 commit `24a945c5a31a03981303e75dd25e5ccb220f6882`.
- Current commit: run `git log -1 --format=%H` in the repository; the handoff reply includes the exact SHA.
- Services: crm, db, daemon, websocket, minio, mailpit. minio-init is a successful one-shot initializer, not a persistent service.

Run `scripts/local credentials` and open **`.local/test-credentials.md`** for the exact passwords. Finder: Cmd+Shift+G, paste the repository path ending `/nurivoyage/.local`, then open test-credentials.md. The private sheet and `.env` are ignored. Role passwords use DEV_USER_PASSWORD; `scripts/local reset-passwords` reapplies that value. No credentials are in this checklist. Log out through the user menu between roles.

| Role | Username |
|---|---|
| System Administrator | admin@nuri.local |
| Sales Agent | sales@nuri.local |
| Operations | operations@nuri.local |
| Sales + Operations Hybrid | hybrid@nuri.local |
| Sales + Operations Commercial | hybrid-commercial@nuri.local |
| Finance | finance@nuri.local |
| Management | manager@nuri.local |

## Exact tests

| # | Test and exact actions | Result | Notes |
|---|---|---|---|
| 1 | Open http://localhost:8080 logged out. Confirm the original UTNT logo, NuriVoyage name, Travel Management Platform descriptor, Nuri's Travel reference and readable Username/Password labels. Page canvas must be **#C2F9FF**, button royal blue, gold accents restrained. Check plane favicon after a hard refresh. Check browser theme colour where your browser supports it; desktop tab-strip colour may be controlled by the browser. Legal EspoCRM notice remains. | PENDING | |
| 2 | Log in as admin@nuri.local. Open Sales → Bookings, then a synthetic Booking, then Create Booking (cancel without saving if no changes needed). Confirm logo proportions, readable headings/tables/forms, visible keyboard focus, blue primary buttons, selected navigation state and cyan canvas. Groups are Sales, Operations, Purchasing & Finance and Workspace. No fake Reports/Management Dashboard link should appear. Customer modules are labelled Customers. | PENDING | |
| 3 | Log in as sales@nuri.local. Open Leads, Enquiries, Customers, Quotes, Bookings, customer invoices/payments and own Commissions. Supplier Bills/Payments, Purchase Orders and FX should be absent from the menu and unreadable by direct route. Open a Booking Item: purchase cost, currency and converted cost must be absent. Create/edit a synthetic customer if desired. | PENDING | |
| 4 | Log in as operations@nuri.local. Confirm Bookings/Items, Travellers, Flights, Hotels, Transfers, Visas, Travel Documents and Suppliers remain usable. Customer/Contact references are read-only. Open/create a Traveller linked to a synthetic Customer, then cancel or save synthetic data. No supplier purchase costs or agent commissions should appear. | PENDING | |
| 5 | Log in as hybrid@nuri.local. Confirm Sales plus Operations navigation and combined workflow. Supplier costs, bills/payments, full creditor/profitability access and other agents' commissions must stay blocked. | PENDING | |
| 6 | Log in as hybrid-commercial@nuri.local. Open Booking Items and verify purchase costs are available. Purchase Orders and Supplier Bills are available. Supplier Payments, FX, company profitability and other agents' commissions remain unavailable. | PENDING | |
| 7 | Log in as finance@nuri.local. Confirm customer invoices/payments, purchase orders, supplier bills/payments, FX and commissions/payment status remain accessible. Check existing edit restrictions on commission rules/amount/beneficiary. Styling must not hide necessary controls. | PENDING | |
| 8 | Log in as manager@nuri.local. Confirm all real commercial modules/costs/commissions are available. Open Home: existing dashboard panels should be readable and consistently styled. Full profitability/reporting remains later scope, with no invented figures. Inspect the three NuriVoyage Email Templates in Workspace. | PENDING | |
| 9 | Test at approximately 1440×900, 1280×800, 768×1024 and 390×844 (browser responsive mode is acceptable for size checks). Verify login fits, button is tappable, navigation expands, forms are readable and page has no horizontal overflow. Native lists may scroll internally or reduce columns. The sidebar may collapse automatically below 1320px; labelled icons and the toggle should remain usable. For an actual phone on the LAN, follow the optional LAN steps in the Stage 2 checklist (temporarily BIND_ADDRESS=0.0.0.0, APP_URL/WS_URL with Mac LAN IP, recreate and bootstrap; revert afterwards). Record actual-device testing separately if not performed. | PENDING | |
| 10 | Open http://localhost:8025 and inspect the three “NuriVoyage Stage 3” synthetic quotation/invoice/purchase-order emails created by smoke tests. Confirm NuriVoyage/company header, original logo, local sender, subject, royal blue/gold/cyan presentation, legible mobile width, HTML and plain-text fallback. You may send a further synthetic email to uat@nuri.local through Espo. SMTP must remain Mailpit only; use no real addresses or external delivery. | PENDING | |
| 11 | Open the three PDF-layout URLs above. Check the company logo, document-number/date block, customer/supplier block, line-item table, totals and footer/terms placeholders. Print preview should use A4 white paper. Sales Pack is absent, so these are clearly labelled design specifications/previews, not generated financial PDFs. Do not approve invented registration/VAT/bank/address details; placeholders must remain until approved information is supplied. | PENDING | |
| 12 | Run `scripts/local stop` then `scripts/local start`. Confirm branding, users, synthetic records and documents persist and `scripts/local health-check` passes for all six services. Refresh the browser to load current assets. Record UI, accessibility, permission or workflow defects below; leave the stack running. | PENDING | |

## Acceptance record

Tester: ______  Date/time/timezone: ______  Browser/OS/devices: ______

Actual LAN phone test: PASS / FAIL / NOT PERFORMED (reason: ______)

Overall: PENDING / PASS / FAIL / CHANGE REQUESTED

Defects/change requests (test number, role, route, expected and observed): ______

Explicit Stage 3 acceptance / requested changes: ______

No passwords, auth tokens, real passport/customer documents or sensitive screenshots should be included in shared UAT evidence.

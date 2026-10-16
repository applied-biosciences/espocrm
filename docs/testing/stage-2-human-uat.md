# Stage 2 human localhost UAT

Status: **PENDING — a human must perform and record this checklist.** Automated API/browser testing does not mark this passed.

## URLs and credentials

- CRM: http://localhost:8080
- Mailpit captured messages: http://localhost:8025 (no login locally)
- MinIO console: http://localhost:9001 (credentials in the private sheet)
- WebSocket endpoint: ws://localhost:8081

From the repository root, run `scripts/local credentials`, then open `.local/test-credentials.md`. It contains the exact passwords generated on this Mac. The file is ignored and mode 0600; passwords are not checked into this document. All seven role accounts use the local `.env` value `DEV_USER_PASSWORD`:

| Role | Login |
|---|---|
| System Administrator | admin@nuri.local |
| Sales Agent | sales@nuri.local |
| Operations | operations@nuri.local |
| Sales + Operations Hybrid | hybrid@nuri.local |
| Sales + Operations Commercial | hybrid-commercial@nuri.local |
| Finance | finance@nuri.local |
| Management | manager@nuri.local |

Reset all role passwords to the current `.env` value: `scripts/local reset-passwords`. To choose a new one, edit DEV_USER_PASSWORD in `.env`, run `docker compose up -d --force-recreate crm` so the container receives it, then run `scripts/local reset-passwords` and `scripts/local credentials`. Do not include passwords in UAT evidence or issues. The separate bootstrap maintenance account uses ESPO_ADMIN_USERNAME/ESPO_ADMIN_PASSWORD. Setting `.env` alone does not reset an existing password.

Log out between role tests (top-right user menu → Log Out), or use separate private browser sessions. Module links can be entered directly: `http://localhost:8080/#NvBooking`, `#NvBookingItem`, `#NvCommission`, `#NvTravelDocument`, `#NvPurchaseOrder`, `#NvSupplierBill`, `#NvSupplierPayment`, `#NvFxRate`, `#Account`, `#Contact`, `#NvEnquiry`.

## Exact acceptance checklist

1. [ ] Open http://localhost:8080. Confirm the login form renders without a blank page or browser error; NuriVoyage application title and EspoCRM legal notice remain visible.
2. [ ] Log in as `admin@nuri.local`. Confirm Administration and all prepared business modules are available; open Bookings and see the three synthetic scenarios.
3. [ ] Log in as `sales@nuri.local`. Confirm Accounts, Contacts, Leads, Enquiries, Quotes, Bookings, Booking Items, Packages, Customer Invoices/Payments and own Commissions are accessible.
4. [ ] As Sales, open an Umrah Booking Item. Confirm purchase cost and purchase-cost currency are absent. Try `#NvPurchaseOrder`, `#NvSupplierBill`, `#NvSupplierPayment`, `#NvFxRate`: no restricted records should be readable. Commissions must exclude “Other agent commission”. There is no profitability/margin dashboard in this baseline.
5. [ ] Log in as `operations@nuri.local`. Confirm Bookings, Booking Items, Travellers, Travel Documents, Hotels, Flights, Transfers, Visas, Suppliers and Packages are available, with read-only Account/Contact reference access. Open a Booking Item: no purchase cost. Finance and Commission modules are unavailable.
6. [ ] Log in as `hybrid@nuri.local`. Confirm both Sales modules (Enquiry/Quote/customer payments) and Operations modules (Traveller/Hotel/Flight/Travel Document) are available. No purchase cost, supplier bills/payments or full creditor access. Only the hybrid user's assigned commission is visible.
7. [ ] Log in as `hybrid-commercial@nuri.local`. Confirm both Sales and Operations modules. Open a Booking Item and verify purchaseCost in USD/SAR is visible. Purchase Orders/Supplier Bills are accessible. Supplier Payments, FX and other agents' commissions are unavailable; no full creditor or management profitability dashboard exists.
8. [ ] Log in as `finance@nuri.local`. Open Customer Invoices/Payments, Purchase Orders, Supplier Bills/Payments, FX and Commissions. Verify commission payment status is editable but beneficiary, method, rule snapshot and amount cannot be changed. Debt/credit transaction records exist; computed ledger/reporting totals are later scope.
9. [ ] Log in as `manager@nuri.local`. Confirm access to all prepared commercial modules, all commission records and purchase costs. Note profitability calculations/report dashboards are documented future implementation, so do not expect computed gross profit/margin yet.
10. [ ] Compare visible navigation with the role matrix in `docs/nurivoyage/stage-1-design.md`. Open each permitted module at least once; record any blank screen, unexpected item or denied legitimate access. System Administrator is a privileged Espo admin and inherently sees commercial data.
11. [ ] As Sales or Management, open Accounts → Create. Enter “UAT Synthetic Customer”, save, edit its description and save again. Add a synthetic Contact linked to this Account. Do not enter any real customer information.
12. [ ] Open/create a Booking or Quote. Confirm ZAR is selected initially and ZAR, USD, GBP, EUR, SAR, AED are available in the amount currency selector. Verify dates display DD/MM/YYYY. As admin inspect Administration → Currency and Settings to confirm base currency ZAR and configured timezone.
13. [ ] Open an Enquiry and move its status through Qualified → Quote Prepared → Quote Sent → Follow-up → Customer Accepted → Deposit Requested → Deposit Paid → Booking Confirmed. Verify Lost, Cancelled and Expired Quote are also options. These are manual states; no automatic payment/confirmation action is expected yet.
14. [ ] As Hybrid Commercial or Management, open a Purchase Order and inspect the supplier states from Booking Confirmed through Paid. Link it to a Booking and Supplier; save an illustrative USD amount. Verify relationships reopen the intended records.
15. [ ] As Operations, open Travel Documents → Create, name it “SYNTHETIC UAT Itinerary”, choose a Booking/Traveller and upload a synthetic PDF/PNG. Save, download and compare the file. Log out: the protected download must no longer work without authentication. Sales must not read the document by direct link. Chunked uploads may first stage locally before the daemon moves them to MinIO; allow one scheduler cycle.
16. [ ] As admin, open Administration → Group Email Accounts → NuriVoyage Local Mailpit and confirm SMTP host mailpit, port 1025, no authentication/TLS, local sender. Alternatively compose an Email to `uat@nuri.local`, subject “NuriVoyage Human UAT”, send it. Open http://localhost:8025 and confirm subject, sender, recipient and body. No real email address is required.
17. [ ] Optionally test a phone/tablet on the same LAN: by default services bind to 127.0.0.1 and are not reachable from LAN. To enable temporarily, set BIND_ADDRESS=0.0.0.0 , APP_URL=http://MAC_LAN_IP:8080 and WS_URL=ws://MAC_LAN_IP:8081 in `.env`, recreate containers with `docker compose up -d --force-recreate`, then run `scripts/local bootstrap`. Test login, navigation, record edit and file download at phone/tablet widths. Revert to localhost/bind 127.0.0.1 afterwards. Mark SKIPPED if impractical.
18. [ ] Run `scripts/local stop`, then `scripts/local start` (or restart Docker Desktop and wait for services). Reopen the UAT customer/contact and synthetic document. Confirm saved edits and file bytes persist. Do not use reset-local during this check.
19. [ ] Run `scripts/local health-check`; all six services and HTTP probes should PASS. Record browser, OS/device, tester, date/time, each role tested, and any UI/permission/workflow defects with synthetic record IDs. Omit passwords and document contents from shared evidence.
20. [ ] Complete the results below. Mark human UAT PASSED only after required checks pass; record optional LAN skip explicitly. Keep the stack running for review. Report defects before approving/merging the PR.

## Human results — fill in after testing

Tester: ______  Date/time/timezone: ______  Browser/device: ______

Overall: PENDING / PASSED / FAILED

Optional LAN: PENDING / PASSED / SKIPPED (reason: ______)

Defects (role, route, synthetic record ID, expected, observed): ______

Permission notes: ______

Human approval: ______

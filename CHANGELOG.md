# Changelog

## v10.0.10.0.s14 — Stage 11 development

- Added commission numbers, basis amounts, frozen rule snapshots, approval and paid timestamps, and settlement references.
- Added Stage 11 commission approval, freeze and settlement smoke coverage and advanced the application marker to `v10.0.10.0.s14`.

## v10.0.10.0.s7 — Stage 7 development

## v10.0.10.0.s8 — Stage 8 development

- Added supplier contact details, codes and active status.
- Added reusable products with supplier, service type, destination, rates and validity dates.
- Added CSV bulk import for airline and hotel catalogue rows with required-column validation and dry-run support.

## v10.0.10.0.s9 — Stage 9 development

- Added PO numbers, supplier references, request and confirmation timestamps to purchase orders.
- Added Stage 9 procurement lifecycle smoke coverage and advanced the application marker to `v10.0.10.0.s9`.

## v10.0.10.0.s10 — Stage 10 development

- Added invoice numbers, paid and balance amounts, payment numbers, deposit/payment/refund types and allocation amounts.
- Added Stage 10 invoice and payment lifecycle smoke coverage and advanced the application marker to `v10.0.10.0.s10`.

- Fixed the Customer page crash caused by a nonexistent linked-list field view, and placed Group Travellers in the native relationship panel.
- Rendered City Stops, Travellers, Transfers and Sightseeing as working itinerary relationship panels, with a complete add-city form and dated stop list.
- Added an idempotent synthetic four-city family fixture for local UAT.
- Linked priced hotel stays to individual city stops, allowing multiple hotels in one city and showing hotel costs on both city and itinerary pages.
- Added Travellers to the Sales menu and visible, searchable Customer and Traveller numbers. A traveller can be linked from the Customer's Group Travellers panel by traveller number, or from the Traveller form by customer number.
- When a group member is unlinked from a Customer, also clear their booking link and lead-traveller designation for that customer's booking.
- Added Booking traveller management: create a new traveller with the Booking prefilled, or select an existing traveller by Traveller Number. Linked members are immediately listed on the Booking page.

- Added a private passport photo attachment to traveller records.
- Added booking reference, itinerary, route, traveller-count and confirmation fields.
- Added multi-city itinerary cities, inter-city transfers with type and cost, multiple hotel stays by city and sightseeing activities with city/date/cost.
- Added Operations-menu itineraries with expandable city segments (two initial cities plus unlimited additions), priced air/road/train transfers, and booking-page transfer/sightseeing panels.
- Added booking-to-traveller linked lists with add/remove controls for group members before final confirmation.
- Added the same group traveller relationship to Customer records and expanded city transfer choices to Car and Bus with arrival/departure dates.
- Made traveller records and passport photos readable by all named application roles, including Sales.
- Added the family/group booking model: Customer billing account, Lead Traveller, member Travellers and shared Group Reference.
- Added the passport photo to the traveller detail page and Stage 7 UAT.
- Updated login and application-page version markers to `v10.0.10.0.s7`.
- Recorded Stage 6 acceptance.

## v10.0.10.0 — Stage 6 development

- Added quote number, option name, sent-at, accepted-at and lost-reason fields.
- Added native quote layouts and sales-pipeline labels.
- Added the `v10.0.10.0` marker to the login page and application pages.
- Recorded Stage 5 acceptance and added Stage 6 localhost UAT materials.

## Stage 5 — Traveller and document metadata

- Added passport identity fields to travellers.
- Added document issuing metadata, verification status and verification attribution.
- Preserved private MinIO-backed document storage and role boundaries.

## Stage 4 — Leads and enquiries

- Added enquiry source, contact, destination, service, budget, follow-up and lost-reason fields.
- Added focused enquiry lifecycle checks and localhost UAT.

## Stage 3 — Branding and responsive UI

- Added UTNT logo, plane favicon, NuriVoyage theme, cyan page canvases, royal-blue controls and gold accents.
- Added grouped role-aware navigation, branded login, email templates and PDF layout foundations.

## Stage 1–2 — Local foundation

- Added the NuriVoyage business model, seven roles, synthetic seed data and local Docker stack.
- Added MariaDB, daemon, WebSocket, MinIO, Mailpit, backups, restore, health checks and automated smoke tests.

## v10.0.10.0.s14 — Stage 12 development

- Added document lifecycle controls for expiry alerts, verification history, retention rules and checklist status.
- Added PDF-ready and printable document flags for local download/printing workflows.

## v10.0.10.0.s14 — Stage 13 development

- Added role-safe profitability, sales, operations, supplier, debtor, creditor and performance report records.
- Added synthetic local report dashboards and Purchasing & Finance navigation entry.

## v10.0.10.0.s14 — Stage 14 development

- Added reusable communication records with email templates, customer communication history and future WhatsApp/SMS channel states.

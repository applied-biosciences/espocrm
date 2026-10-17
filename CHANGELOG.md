# Changelog

## v10.0.10.0.s7 — Stage 7 development

- Added a private passport photo attachment to traveller records.
- Added booking reference, itinerary, route, traveller-count and confirmation fields.
- Added multi-city itinerary cities, inter-city transfers with type and cost, multiple hotel stays by city and sightseeing activities with city/date/cost.
- Made traveller records and passport photos readable by all named application roles, including Sales.
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

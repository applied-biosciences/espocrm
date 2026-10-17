# NuriVoyage Stage 7 Travellers and Passport Photos

Stage 7 delivers the planned bookings and itineraries foundation, adds a private passport-photo attachment to each traveller record, and advances the application version to `v10.0.10.0.s7`. It remains local-only, uses synthetic data and images only, preserves the Stage 1–6 role boundaries and does not deploy to AWS or send external email.

## Scope

- Add a passport photo file field to `NvTraveller`.
- Display the field on the traveller detail page with the existing private attachment controls; traveller records and this photo are readable by all named application roles, including Sales.
- Add booking reference, itinerary title, destination, route, traveller count, notes and confirmation timestamp to `NvBooking`.
- Support a city sequence, multiple hotel stays in the same itinerary, inter-city transfer type/cost and one or more sightseeing activities with city and cost.
- Support family/group bookings with one Lead Traveller and separate member Traveller records linked to the same booking and Group Reference.
- Display the itinerary fields on the native booking detail and list pages.
- Keep the head-and-shoulders photo requirement in human UAT guidance; do not use real identity photos.
- Update login, application-page and changelog version markers to `v10.0.10.0.s7`.
- Run full regression and focused Stage 7 checks.

## Out of scope

Face recognition, automated image validation, OCR, public image URLs, real passports, customer portal, AWS and external integrations.

## Acceptance

Stage 7 is ready when a synthetic head-and-shoulders passport photo can be attached to and viewed on a traveller record by Operations and Sales, a synthetic itinerary can be created and reviewed by Operations, the separate travel-document module remains protected, the version marker is visible and all smoke tests pass.

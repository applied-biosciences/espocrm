# NuriVoyage Stage 5 Customers Travellers and Documents

Stage 5 turns the existing customer, traveller and travel-document foundations into a usable operational record. It is local-only, uses synthetic data, preserves Stage 1–4 role boundaries and does not deploy to AWS or send external email.

## Scope

- Add passport number, country, issue date and expiry date to `NvTraveller`.
- Add document number, issuing country, issue date and verification status to `NvTravelDocument`.
- Record verified-at and verified-by metadata for document review.
- Expose the new fields in native detail and list layouts.
- Keep travel documents available to Operations and Management while Sales remains excluded from the travel-operations scopes.
- Run the full Stage 2 regression and focused Stage 5 checks.

## Out of scope

OCR, automated passport validation, real identity documents, customer portal access, external storage, AWS, WhatsApp/SMS and automated expiry notifications.

## Acceptance

Stage 5 is ready when synthetic traveller and document records can be created and reviewed through the authenticated API, the verification status persists, role boundaries remain intact, existing smoke tests pass and the local UAT checklist is available.

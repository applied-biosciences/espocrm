# NuriVoyage Stage 4 Leads and Enquiries

Stage 4 turns the Stage 1 enquiry foundation into an operational lead and enquiry workflow. It remains local-only, uses synthetic data, preserves the Stage 1–3 role boundaries, and does not deploy to AWS or send external email.

## Scope

- Extend `NvEnquiry` with source, source detail, contact, destination, service type, preferred contact method, budget, next follow-up and lost reason.
- Preserve the existing audited sales statuses and native Lead integration.
- Keep Sales Agent, Hybrid and Commercial roles able to create and manage enquiries; Operations retains the existing read-only customer/reference boundary.
- Make the fields visible in the native detail and list layouts.
- Rebuild metadata, run the full Stage 2/3 regression, and run Stage 4 API checks.
- Provide a localhost human UAT checklist for lead capture, assignment, follow-up and terminal statuses.

## Out of scope

Automated status transitions, quote generation, payment reconciliation, WhatsApp/SMS delivery, production data, external email, AWS and the Stage 13 management dashboard.

## Acceptance

Stage 4 is ready when the new fields can be created and read through the authenticated API, role access remains consistent, existing smoke tests pass, and the local UAT checklist is available.

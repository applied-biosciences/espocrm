# NuriVoyage Stage 6 Quotes and Sales Pipeline

Stage 6 turns the existing quote foundation into a clearer sales pipeline record. It remains local-only, uses synthetic data, preserves the Stage 1–5 role boundaries and does not deploy to AWS or send external email.

## Scope

- Add quote number, option name, sent-at, accepted-at and lost-reason fields.
- Preserve the existing Draft, Sent, Accepted, Lost, Cancelled and Expired Quote statuses.
- Expose the new fields in native detail and list layouts.
- Add a small version marker, `v10.0.10.0`, to the login page and every application page.
- Keep quote access within the existing Sales, Hybrid, Commercial, Finance and Management boundaries.
- Run full regression and focused Stage 6 checks.

## Out of scope

Automatic quote numbering, PDF generation, payment reconciliation, external email, customer portal, AWS and full financial posting.

## Acceptance

Stage 6 is ready when synthetic quotes can move through the sales statuses with the new fields persisted, the version marker is visible on login and application pages, existing smoke tests pass and the local UAT checklist is available.

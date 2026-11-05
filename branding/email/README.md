# Local email foundation

Quotation, Invoice and Purchase Order each have an HTML foundation and a plain-text source. Bootstrap creates three native Active EmailTemplate records, available to administrators and Management. Other role grants remain unchanged. They contain explicit [[...]] placeholders, not an automatic booking/invoice/PO workflow. Fill approved synthetic values before testing; do not send unresolved templates to real recipients.

HTML uses a 600px maximum-width presentation table, mobile-compatible widths, original logo from APP_URL, royal-blue/NuriVoyage header and company signature placeholders. The test supplies an explicit native Email.bodyPlain alternative and verifies both MIME representations in Mailpit. Native email templates support HTML; the separate .txt source is available to a future workflow adapter.

System sender: NuriVoyage · Nuri's Travel (LOCAL), admin@nuri.local. Only SMTP_HOST=mailpit / SMTP_PORT=1025 is allowed by the local bootstrap. IMAP is disabled; Mailpit has no upstream relay and SMTP is not published to the host. No production SMTP configuration is added.

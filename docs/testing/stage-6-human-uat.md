# Stage 6 human localhost UAT

URL: http://localhost:8080

Use the synthetic credentials in `.local/test-credentials.md`.

1. Confirm `v10.0.10.0` is visible on the login page.
2. Log in as `sales@nuri.local` and create a synthetic quote linked to an enquiry and customer.
3. Enter quote number, option name, selling price and valid-until date.
4. Move the quote from Draft to Sent and enter the sent-at timestamp.
5. Move a test quote to Accepted and enter the accepted-at timestamp.
6. Move another test quote to Lost and record a lost reason.
7. Confirm the quote list shows quote number, status, valid-until date and assigned user.
8. Confirm `v10.0.10.0` remains visible after login on a normal application page.
9. Confirm the Stage 3 branding and responsive layout remain intact.

Record PASS, FAIL or CHANGE REQUESTED for each item before accepting Stage 6.

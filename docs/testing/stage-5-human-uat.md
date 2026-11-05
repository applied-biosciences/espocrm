# Stage 5 human localhost UAT

Status: **ACCEPTED**. The user accepted Stage 5 in chat after the automated checks and localhost review.

URL: http://localhost:8080

Use the synthetic credentials in `.local/test-credentials.md`. Do not upload real passports or identity documents.

1. Log in as `operations@nuri.local` and create a synthetic traveller linked to a local customer and booking.
2. Enter nationality, passport number, issuing country, issue date and expiry date; save and refresh.
3. Create a synthetic travel document linked to the traveller and booking, choosing a document type and verification status.
4. Attach only a synthetic test file, then confirm the document remains private and downloadable by the authorised Operations user.
5. Change the verification status from Pending to Verified or Rejected and confirm it persists.
6. Confirm the traveller list shows nationality and passport expiry date.
7. Confirm the document list shows type, expiry date and verification status.
8. Log in as `sales@nuri.local` and confirm travel documents are not available through the Sales navigation or API.
9. Confirm the Stage 3 branded layout and responsive behaviour remain intact.

Record PASS, FAIL or CHANGE REQUESTED for each item before accepting Stage 5.

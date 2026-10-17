# Stage 4 human localhost UAT

URL: http://localhost:8080

Use the synthetic credentials in `.local/test-credentials.md`. Do not enter real customer details.

1. Log in as `sales@nuri.local` and create an enquiry with source, service type, destination, preferred contact method, traveller count, budget and next follow-up.
2. Link the enquiry to a synthetic customer, contact or native Lead and confirm the links display after saving.
3. Edit the enquiry and move it through Qualified, Quote Prepared, Quote Sent and Follow-up.
4. Confirm the enquiry list shows status, source, service type, next follow-up and assigned user.
5. Assign the enquiry to a permitted sales user and verify the assignment persists after refresh.
6. Set a terminal status such as Lost and record a lost reason.
7. Repeat a read-only reference check as `operations@nuri.local`; confirm customer/reference access remains read-only.
8. Confirm the Stage 3 branded layout, cyan page canvas, royal-blue controls and gold accents remain intact.

Record PASS, FAIL or CHANGE REQUESTED for each item before accepting Stage 4.

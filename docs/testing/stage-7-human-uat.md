# Stage 7 human localhost UAT

URL: http://localhost:8080

Use the synthetic credentials in `.local/test-credentials.md`. Use only a synthetic head-and-shoulders test image; do not upload a real passport photo.

1. Confirm the login page displays `v10.0.10.0.s7`.
2. Log in as `operations@nuri.local` and open or create a synthetic traveller.
3. Attach a small synthetic head-and-shoulders passport-style image in the Passport Photo field.
4. Save and refresh the traveller; confirm the photo remains visible on the traveller detail page.
5. Confirm the photo is private and accessible only through the authorised CRM record.
6. Confirm `v10.0.10.0.s7` remains visible after login on an application page.
7. Log in as `sales@nuri.local` and confirm the traveller record and passport photo are visible, while the separate travel-document operations module remains excluded.
8. Confirm the Stage 3 branded layout and responsive behaviour remain intact.
9. Create a synthetic booking and enter booking reference, itinerary title, destination, departure city, arrival city, traveller count and itinerary notes.
10. Confirm the itinerary fields persist after refresh and are visible on the booking list/detail pages.
11. Add two hotel stays in different cities and confirm both remain linked to the booking with their city and stay sequence.
12. Add an Inter-city transfer between two itinerary cities and enter its transfer cost.
13. Add one or more sightseeing activities in an itinerary city and enter each activity cost.
14. For a family/group booking, confirm the customer is the billing/customer account, the booking has one Lead Traveller, and every group member is a separate Traveller linked to the same booking and Group Reference.

Record PASS, FAIL or CHANGE REQUESTED for each item before accepting Stage 7.

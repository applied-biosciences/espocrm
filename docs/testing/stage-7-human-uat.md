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
15. Open the [synthetic Al Noor family customer](http://localhost:8080/#Account/view/6ad3415bbf5bbc925). Confirm the Customer page opens and Group Travellers lists four members with their booking and lead-traveller status.
16. Click **+** in Group Travellers. Confirm the add form includes Name, Customer, Booking, Group Reference and Lead Traveller. Cancel without saving.
17. Open a group member's row menu and confirm **Unlink** is available. Do not unlink the demonstration member during UAT unless you plan to relink it.
18. Open the [synthetic four-city itinerary](http://localhost:8080/#NvBooking/view/6ad3415c364483e5e). Confirm City Stops shows Jeddah, Makkah, Madinah and Riyadh, each with arrival/departure dates, incoming transfer method and cost.
19. Click **+** in City Stops. Confirm the add form includes City Sequence, City, Arrival Date, Departure Date, Transfer From, Transfer Mode, Transfer Cost and Currency. Cancel without saving.
20. Confirm the itinerary shows the four travellers, three inter-city transfers and two sightseeing activities in related-record panels.
21. Confirm **Hotels by City** lists five hotel stays, with at least one in every city, two in Makkah, and a cost and check-in/out dates for each stay.
22. Open each City Stop. Confirm **Hotels in This City** lists only that city's hotels and shows their costs. Click **+** in the Makkah hotel panel and confirm a new hotel form includes the city stop, dates and cost; cancel without saving.
23. Open **Sales → Travellers**. Confirm **Create Traveller** is available and Traveller Number appears in the list and detail page. Open the create form, type Customer Number `29` into Customer, and confirm `DEMO Al Noor Family (synthetic)` appears as a suggestion. Cancel without saving.
24. On the synthetic Customer, confirm Customer Number `29` is visible. In **Group Travellers → ⋮ → Select**, search for an unlinked Traveller Number (the local demo currently has several); confirm the matching traveller appears. Cancel without linking.
25. Confirm the synthetic Customer's four linked traveller numbers `33`–`36` appear in Group Travellers. To verify a real link/unlink, use a disposable synthetic traveller rather than one of these four demonstration members.
26. On the synthetic itinerary, use **Travellers → +** and confirm the new traveller form has the Booking prefilled; cancel without saving. Use **Travellers → ⋮ → Select**, search by an existing Traveller Number, select it and confirm it appears in the Booking manifest. Remove the disposable test link afterward if required.

Record PASS, FAIL or CHANGE REQUESTED for each item before accepting Stage 7.

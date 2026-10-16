# NuriVoyage Stage 1 design — schema v1

Product: **NuriVoyage**. Company: **Nuri's Travel**. EspoCRM 10.0.10, MariaDB 11.4.5. Stage 1 defines and prepares the business model; Stage 2 proves a reproducible local foundation. No AWS provisioning. No purchased Espo extensions required.

## Organisation defaults

Reporting/base/default currency ZAR; enabled ZAR, USD, GBP, EUR, SAR, AED. Date DD/MM/YYYY. Timezone comes from `APP_TIMEZONE` (default Africa/Johannesburg). Bootstrap contains deliberately synthetic illustrative exchange rates, never live rates or accounting advice. Amounts retain their original currency. Future valuation must snapshot the applicable FX rate/date/source on posting.

## Entities and relationships

Use native Account (customer), Contact and Lead. Native Email, Task and Document remain available where permitted. Travel entities use the `Nv` prefix to avoid collisions with future paid extensions. All are standard Espo Base entities, with name, description, timestamps, creator/modifier, assigned user and teams. Every custom field is versioned in `custom/Espo/Custom/Resources/metadata/entityDefs/*.json`; detail/list layouts and labels are also versioned. Link fields use actual belongs-to ORM relationships, not text IDs. The baseline follows links from child to parent; inverse subpanels can be added later.

| Entity | Fields beyond common fields / relationship targets |
|---|---|
| Account / Contact / Lead | Native customer, person and prospective customer model; Contact → Account |
| NvEnquiry | customer → Account, lead → Lead, status, travelDate, travellerCount |
| NvTraveller | customer → Account, booking → NvBooking, dateOfBirth, nationality |
| NvQuote | enquiry, customer, booking, status, sellingPrice + currency, validUntil |
| NvBooking | customer, enquiry, package, sales status, supplierStatus, sellingPrice + currency, travelDate, returnDate |
| NvBookingItem | booking, supplier, productType, sellingPrice + currency, purchaseCost + currency, supplierStatus |
| NvSupplier | emailAddress, phoneNumber, category |
| NvPurchaseOrder | booking, supplier, status, amount + currency, dueDate |
| NvSupplierBill | booking, supplier, purchaseOrder, status, amount + currency, dueDate |
| NvCustomerInvoice | booking, customer, status, amount + currency, dueDate |
| NvCustomerPayment | booking, customer, customerInvoice, amount + currency, paymentDate, reference |
| NvSupplierPayment | booking, supplier, supplierBill, amount + currency, paymentDate, reference |
| NvCommission | booking, assignedUser = beneficiary, method, amount + currency, status, ruleSnapshot |
| NvFxRate | fromCurrency, toCurrency, rate, rateDate |
| NvTravelDocument | booking, traveller, file (Espo attachment), documentType, expiryDate |
| NvHotel | booking, supplier, bookingItem, checkIn, checkOut, confirmation |
| NvFlight | booking, supplier, bookingItem, departure, flightNumber, route, confirmation |
| NvTransfer | booking, supplier, bookingItem, pickupAt, pickupLocation, confirmation |
| NvVisa | booking, supplier, traveller, bookingItem, status, country |
| NvPackage | destination, sellingPrice + currency, durationDays |

Currency fields produce companion `...Currency` attributes and framework reporting fields. Bootstrap explicitly denies purchaseCost, purchaseCostCurrency and purchaseCostConverted for restricted roles; the generated converted field does not automatically inherit the base field restriction in this version. All statuses are explicit selectable, audited baseline states. These are preparatory CRUD records, not a posted accounting ledger.

## Workflows

Sales: New Enquiry → Qualified → Quote Prepared → Quote Sent → Follow-up → Customer Accepted → Deposit Requested → Deposit Paid → Booking Confirmed. Terminal states: Lost, Cancelled, Expired Quote. Enquiry and Booking expose this vocabulary; Quote has Draft/Sent/Accepted/Lost/Cancelled/Expired Quote.

Supplier: Booking Confirmed → Supplier Selected → Purchase Order Created → PO Emailed → Supplier Confirmation → Supplier Invoice Received → Payment Due → Paid. Booking, Booking Item and Purchase Order expose the baseline. Supplier Bill has Received/Payment Due/Paid/Cancelled.

At this stage users move statuses manually. Transition validation, deposit reconciliation, PO generation/email automation, reminders, approvals and cancellation accounting are later work. A PO Emailed status does not itself send email.

## Permissions

Roles default-deny every ACL-enabled native/custom scope; then explicitly permit the appropriate entities. API access and field ACL enforce restrictions; navigation alone is not the security boundary. Delete/export/mass-update are disabled for development business roles. Agents can read their own User record so default self-assignment on record creation works; Management/Finance can read user identities. Assignment permission is denied for agents so they cannot reassign others' commission records to themselves; Management can assign business records. The role bootstrap resets each synthetic user's role set to exactly one role. Do not add permissive extra roles: Espo combines grants additively.

| Role | Access | Denials / limits |
|---|---|---|
| Sales Agent | Accounts, Contacts, Leads, Enquiries, Quotes, Bookings/Items, Packages, customer invoices/payments, Email/Task; own commissions read only | No purchase cost field, PO, supplier bills/payments, FX, travel operations modules or others' commissions |
| Operations | Read-only Account/Contact references; Bookings/Items, Travellers, Travel Documents, Hotels, Flights, Transfers, Visas, Suppliers, Packages, Document, Email/Task | No purchase cost field, PO, bills/payments, commission or finance scopes |
| Sales + Operations Hybrid | Union of Sales and Operations; own commissions read only | No purchase cost field or supplier finance scopes; no other agents' commissions |
| Sales + Operations Commercial | Hybrid plus purchase-cost field, Purchase Orders and Supplier Bills | No Supplier Payments, FX, full creditor reporting, company margin or other agents' commissions |
| Finance | Customer invoices/payments, PO, supplier bills/payments, FX, supplier costs, commissions/payment status, relevant customer and booking records | Commission amount/method/rule/beneficiary/booking cannot be edited; no management profitability dashboard exists in baseline |
| Management | All baseline business entities, costs and commissions | Future profitability calculations/reports are not implemented yet |
| System Administrator | Technical administrator account plus named role | Espo admin bypasses ACL. Technical and commercial separation is documented but cannot be enforced on an Espo superuser. Use manager for daily commercial work; retain admin for maintenance only. |

Sales/Hybrid cannot read purchaseCost, purchaseCostCurrency or reporting equivalents through the API, and cannot write hidden costs. An agent's commission is scoped by assignedUser ownership. Sales/Hybrid can read invoice and payment records; computed customer balances, debtors/creditors roll-ups, financial reports and management dashboards are deferred. The document contains the profitability design for developers; it is not exposed in these users' application navigation.

## Profitability design for later implementation

Selling price minus flight, hotel, transfer, visa, insurance and other direct costs = gross profit. Gross profit minus sales agent commission = net contribution. Gross margin = gross profit / selling price, with a defined zero-sale policy. Convert/snapshot currencies before aggregation. Later calculated values belong in a separate Management-only projection/service, not broadly readable Booking metadata. Finance may access underlying transactions without automatically receiving management reports. Standard Sales/Hybrid must never receive this projection via API, exports, search, streams, dashboards or linked records.

## Commission design for later implementation

Methods: percentage of sale; percentage of gross profit; fixed amount; product-specific rules. An approved posting must freeze method, rule version, rate, product, basis, FX, currency and calculated amount. Subsequent rule edits must affect future bookings only. Corrections require reversals/adjustments rather than mutating history. The v1 amount and ruleSnapshot fields are synthetic preparation only: there is no immutable posted ledger, formula engine or commission payout automation yet. Agents cannot create/edit commission records. Management can edit baseline drafts; future approvals must enforce immutability in server-side hooks and transaction tests.

## Local document and email paths

NvTravelDocument.file → native Attachment → Espo FileStorage Manager → built-in AwsS3 adapter → private MinIO bucket. A small supported custom S3 adapter subclass translates confirmed missing objects into HTTP 404 (the native adapter otherwise returned 500 on a stale deleted-file URL); other storage errors retain their error behavior. It keeps the native AwsS3 storage ID and configuration. Browser downloads through authenticated `/api/v1/Attachment/file/{id}` with record ACL. No public object URL or anonymous bucket policy is used. The same adapter can later use AWS S3 by changing configuration, separately authorised and tested. Browser chunked uploads may stage in Espo data/upload, then the scheduler moves them to the configured object store; backups include both stores. Only synthetic files allowed locally.

A native Group Email Account matching admin@nuri.local provides EspoCRM 10 system SMTP (IMAP disabled). SMTP points only to Mailpit on the Compose network. SMTP is not published to the host. Mailpit has no upstream relay configured. Local sender and recipient addresses end in `nuri.local`.

## Seed and scope limits

Bootstrap creates Ahmed Khan, Fatima Patel, Mohammed Ismail and their Contacts; five named demo suppliers; Umrah Family Package, Dubai Holiday, Cape Town → London flight; related enquiries, quotes, bookings/items, travellers, invoices, POs and commissions. ZAR sales, USD flights/hotels and SAR transfers demonstrate mixed currencies. A separate agent commission is a negative security fixture. Other entity types are ready for manual creation; no real itineraries, stock, live rates, bank integrations, ticketing or production data are involved.

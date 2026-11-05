# NuriVoyage Stage 3 — Branding, UI and Local Acceptance

## Objective
Transform the local EspoCRM development build into a clearly branded **NuriVoyage Travel Management Platform** without breaking Stage 1 or Stage 2 functionality.

Stage 3 is branding, visual identity, navigation polish, login experience, document/email appearance, responsive usability, and basic role-aware UI presentation.

Do not deploy to AWS in this stage.

## Preconditions
1. Stage 1 and Stage 2 must be complete and smoke-tested.
2. Start Stage 3 from the latest approved NuriVoyage development baseline, not from an outdated master snapshot.
3. Create a dedicated implementation branch, recommended:
   `codex/nurivoyage-stage-3`
4. Do not work directly on `master`.
5. Preserve all existing Stage 1 and Stage 2 configuration, data model, roles, local Docker services, MinIO, Mailpit, backup/restore, and smoke-test tooling.

## Brand identity

Application name:
**NuriVoyage**

Descriptor:
**Travel Management Platform**

Company:
**Nuri's Travel**

Primary palette:
- Royal Blue: `#123B7A`
- Deep Navy: `#0B1F3A`
- Gold: `#C9A227`
- Soft Gold: `#E7D59A`
- White: `#FFFFFF`
- Light Background: `#F6F8FB`

Design principles:
- Royal blue is the primary navigation and interface colour.
- Gold is an accent only. Do not use large gold background areas.
- Most content surfaces should remain white or very light grey.
- Text should use dark navy or near-black for readability.
- The interface should feel premium and travel-oriented, not like a generic CRM.
- Maintain accessible contrast for text, navigation, buttons, status badges, tables and forms.

## Scope A — Application identity
Replace user-facing EspoCRM identity where supported through safe customisation mechanisms.

Required:
- Application title: NuriVoyage
- Descriptor: Travel Management Platform
- Company reference: Nuri's Travel
- Browser title where supported
- Login page identity
- Header/app identity
- Favicon placeholder or NuriVoyage icon if an asset is available
- Remove or reduce visible EspoCRM branding where legally and technically permitted

Do not alter licensing notices or legally required attribution.

Do not patch EspoCRM core files merely to hide branding. Prefer supported configuration, metadata, custom frontend, extension mechanisms, themes and upgrade-safe overrides.

## Scope B — Theme
Create a NuriVoyage theme using the approved colour palette.

Apply consistently to:
- top navigation or side navigation
- active navigation state
- primary buttons
- secondary buttons
- links
- headings
- cards/panels
- tables
- tabs
- form controls
- status indicators
- modal windows
- notifications
- login screen

Gold should mainly appear in:
- accents
- selected highlights
- icons
- premium visual details
- small emphasis elements

Do not use gold for ordinary body text.

## Scope C — Login page
Create a polished NuriVoyage login experience.

Required elements:
- NuriVoyage identity
- Travel Management Platform descriptor
- Nuri's Travel reference
- royal blue and white primary presentation
- restrained gold accent
- clean desktop layout
- responsive mobile layout

Do not expose:
- database details
- environment variables
- version/debug information
- internal service names

## Scope D — Navigation
Prepare the navigation to support the planned NuriVoyage operating model.

Preferred visible grouping, where currently available:

### Sales
- Leads
- Enquiries
- Customers
- Quotes
- Bookings

### Operations
- Travellers
- Flights
- Hotels
- Transfers
- Visas
- Travel Documents

### Purchasing / Finance
- Suppliers
- Purchase Orders
- Supplier Bills
- Customer Invoices
- Payments
- Commissions
- FX Rates

### Management
- Management Dashboard
- Reports

Do not create fake functional modules solely to fill the menu.
If a later-stage entity is not yet implemented, document it as planned rather than creating a broken navigation item.

Navigation should respect user permissions.

## Scope E — Role-aware interface
Use the Stage 1 role model:
- Sales Agent
- Operations
- Sales + Operations Hybrid
- Sales + Operations Commercial
- Finance
- Management
- System Administrator

Verify the UI does not present obviously inaccessible finance or management functions to restricted roles where Espo supports role-based navigation visibility.

Critical rule:
Sales users must not gain access to supplier costs, total margin, creditor balances or management profitability merely because of Stage 3 UI changes.

## Scope F — Dashboard presentation
Do not build the full Stage 13 management dashboard yet.

For Stage 3:
- improve the visual presentation of existing dashboard areas
- establish reusable NuriVoyage card styling
- establish heading hierarchy
- establish table styling
- establish status badge conventions

If sample dashboard cards are needed for presentation testing, use synthetic local data only.

## Scope G — PDF branding foundation
Prepare the branding layer for future quote, invoice and purchase-order PDFs.

Where current installed functionality supports PDF templates, create or prepare templates/placeholders using:
- NuriVoyage branding
- Nuri's Travel company name
- royal blue headings
- restrained gold accents
- clean white background
- document number area
- customer/supplier information block
- line-item table style
- totals area
- terms/footer area

Do not invent legal company registration, VAT, bank or address information.
Use clearly marked placeholders where real details are not yet supplied.

If Sales Pack is not installed, create the design/template specification and hooks only. Do not implement duplicate invoice/PO engines.

## Scope H — Email branding foundation
Configure local email templates where functionality exists.

Prepare branded templates for:
- quotation email
- invoice email
- purchase-order email

Local development must send only to Mailpit.
No external email delivery in Stage 3.

Email style:
- clear NuriVoyage header
- minimal design
- mobile-friendly HTML
- plain-text fallback where supported
- Nuri's Travel signature placeholder

## Scope I — Responsive design
Test NuriVoyage at minimum on:
- desktop width approximately 1440px
- laptop width approximately 1280px
- tablet width approximately 768px
- mobile width approximately 390px

Required:
- no horizontal page overflow in core screens
- navigation remains usable
- forms remain readable
- buttons remain tappable
- tables remain usable through supported responsive behaviour
- login screen fits mobile correctly

Do not build native iOS or Android applications.

## Scope J — Accessibility baseline
Verify:
- readable colour contrast
- visible focus states
- labels remain associated with form fields where Espo provides them
- buttons have readable labels/icons
- gold is not used as the sole indicator of state
- error messages remain readable

Record any upstream Espo limitation that prevents full compliance.

## Scope K — Upgrade-safe implementation
Mandatory rules:
1. Prefer Espo supported custom directories, themes, metadata and configuration.
2. Avoid direct edits to upstream core files.
3. If a core edit is unavoidable, stop and document why before proceeding.
4. Keep NuriVoyage branding assets and code clearly separated.
5. Document all custom files.
6. Preserve compatibility with future Espo upgrades as far as practical.

## Scope L — Assets
Create a clear asset structure such as:

```text
branding/
├── logo/
├── favicon/
├── icons/
├── pdf/
└── email/
```

If no final NuriVoyage logo asset exists yet:
- use a clean text-based NuriVoyage placeholder
- do not invent a final logo
- make replacement straightforward

## Automated localhost smoke tests
Codex must run automated smoke tests after implementation and fix failures before requesting human testing.

Minimum tests:

### Smoke 1 — Docker health
- all Stage 2 required containers start
- no required service repeatedly crashes

### Smoke 2 — Application load
- `http://localhost:8080` returns the login application successfully

### Smoke 3 — Branding identity
Verify user-facing page contains NuriVoyage identity in the intended locations.

### Smoke 4 — Login
Log in using a local test administrator account.
Verify successful redirect to authenticated application.

### Smoke 5 — Navigation
Verify primary navigation renders without broken links introduced by Stage 3.

### Smoke 6 — Role regression
Using representative local users, verify restricted roles still cannot access protected finance/management functions.
At minimum test:
- Sales Agent
- Hybrid
- Finance
- Management

### Smoke 7 — Core Stage 2 regression
Verify:
- MariaDB persistence
- MinIO remains reachable
- Mailpit remains reachable
- daemon/worker remains healthy
- websocket remains healthy

### Smoke 8 — Email local-only
Send a NuriVoyage test email through Espo.
Verify it appears in Mailpit.
Verify no external SMTP destination is used.

### Smoke 9 — Restart persistence
Restart Docker Compose.
Verify branding/configuration persists.

### Smoke 10 — Browser assets
Verify no recurring 404s for NuriVoyage CSS, logos, icons or custom JavaScript on login and main application pages.

### Smoke 11 — Responsive checks
Run automated viewport checks where tooling permits for:
- 1440x900
- 1280x800
- 768x1024
- 390x844

Check for obvious horizontal overflow, hidden login controls and inaccessible navigation.

### Smoke 12 — Logs
Review relevant logs for new fatal errors, repeated exceptions or failed custom asset loads.

## Smoke-test result format
Create a report such as:

```text
NURIVOYAGE STAGE 3 SMOKE TEST

PASS Docker health
PASS localhost application load
PASS NuriVoyage branding
PASS admin login
PASS navigation
PASS Sales role regression
PASS Hybrid role regression
PASS Finance role regression
PASS Management role regression
PASS MariaDB regression
PASS MinIO regression
PASS Mailpit regression
PASS worker/daemon
PASS websocket
PASS restart persistence
PASS custom assets
PASS desktop responsive check
PASS tablet responsive check
PASS mobile responsive check
PASS logs
```

Any FAIL must include:
- failure description
- root cause
- fix attempted
- final status

Do not declare Stage 3 complete with unresolved critical smoke-test failures.

## Localhost human acceptance testing
After automated smoke tests pass, leave the local environment running for human review.

Provide:
- exact localhost URL
- Mailpit URL
- MinIO URL if human access is required
- test usernames
- test passwords or safe local credential location
- active Docker services
- branch name
- latest commit SHA

### Human Test 1 — Login appearance
Open localhost.
Check:
- NuriVoyage name is prominent
- Travel Management Platform descriptor is correct
- Nuri's Travel reference is correct
- royal blue/gold/white presentation looks professional
- no inappropriate Espo branding dominates the page

### Human Test 2 — Desktop application
Log in as administrator.
Check:
- navigation is clean
- selected menu state is obvious
- colours are consistent
- buttons are clear
- forms remain easy to read
- tables remain easy to read

### Human Test 3 — Sales Agent
Log in as Sales Agent.
Check:
- sales functions are accessible
- prohibited finance/management information is not visible
- UI does not show confusing inaccessible management areas

### Human Test 4 — Operations
Log in as Operations.
Check:
- operational areas remain usable
- branding does not interfere with workflow

### Human Test 5 — Hybrid
Log in as Sales + Operations Hybrid.
Check:
- combined workflow is practical
- supplier costs and management profitability remain blocked unless explicitly permitted

### Human Test 6 — Hybrid Commercial
Log in as Sales + Operations Commercial.
Check:
- expected commercial operational access works
- full management profitability remains protected

### Human Test 7 — Finance
Log in as Finance.
Check:
- finance areas remain accessible
- restricted management controls remain appropriate

### Human Test 8 — Management
Log in as Management.
Check:
- full commercial visibility remains available
- dashboard presentation is clear

### Human Test 9 — Mobile
From a phone on the same network, open the local NuriVoyage URL.
Check:
- login fits screen
- navigation works
- no major horizontal overflow
- forms are usable
- buttons are large enough to tap

### Human Test 10 — Local email
Trigger a test email.
Open Mailpit.
Check:
- NuriVoyage identity
- email formatting
- subject
- sender presentation
- mobile readability

### Human Test 11 — PDF foundation
If PDF functionality is installed locally, create a synthetic test PDF and check:
- NuriVoyage branding
- layout
- line items
- totals
- footer
- no invented legal/company details

If PDF functionality is not installed, review the stored PDF template specification instead.

### Human Test 12 — Restart
Restart the local stack.
Check:
- branding remains
- configuration remains
- test users remain
- local data remains

## Human acceptance result
Provide a checklist with:
- PASS
- FAIL
- CHANGE REQUESTED

for each human test.

Do not merge Stage 3 until the human tester explicitly accepts the build or requests specified changes.

## Deliverables
At completion provide:
1. implementation branch name
2. commit SHA(s)
3. changed file list
4. branding/theme architecture summary
5. localhost URL
6. local test accounts
7. automated smoke-test report
8. exact human UAT checklist
9. known issues
10. screenshots if practical
11. confirmation that no AWS deployment occurred
12. confirmation that no real customer data was used
13. confirmation that no external emails were sent

## Out of scope for Stage 3
Do not implement the full functionality planned for later stages, including:
- full travel booking engine
- full quote/invoice/PO workflows unless already provided by installed Espo extensions
- automated FX integration
- profitability engine
- commission engine
- WhatsApp integration
- AWS infrastructure
- production S3
- production SMTP
- customer portal
- supplier portal
- native mobile apps

Stage 3 is complete when NuriVoyage looks and behaves like a coherent branded application locally, all Stage 1–2 functionality remains intact, automated smoke tests pass, and the localhost build is ready for human acceptance testing.

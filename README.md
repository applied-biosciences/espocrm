# NuriVoyage — local travel management platform v10.0.10.0.s10

NuriVoyage is Nuri's Travel's local travel-management platform on this EspoCRM fork. The current development line is `codex/nurivoyage-stage-7`; Stage 6 is accepted and Stage 7 is under localhost acceptance. No AWS deployment has been made. Native EspoCRM licensing and legal notices remain intact; upstream documentation follows below.

The application version shown in the login and application pages is `v10.0.10.0.s10`. This is the NuriVoyage application version; the bundled EspoCRM distribution remains pinned to 10.0.10.

## Clone and run

Prerequisites: Docker Desktop/Engine with Compose v2, Git, Python 3 (standard library only), and free localhost ports 8080, 8081, 8025, 9000, 9001. First MinIO source build requires internet access and a few minutes. The Compose image version matches the fork's package.json (10.0.10); there are no core source changes in this stage. It runs the matching official distribution with this checkout's custom directories mounted, rather than building Espo's raw development frontend.

```sh
git clone --branch codex/nurivoyage-stage-1-2 https://github.com/applied-biosciences/espocrm.git
cd espocrm
scripts/local configure
scripts/local start
scripts/local credentials
```

`configure` creates `.env` from `.env.example` with random local passwords and mode 0600. Existing `.env` is preserved. To configure manually, copy `.env.example` to `.env`, replace every CHANGE_ME, and restrict permissions. Never commit `.env`. The first start builds MinIO from a pinned upstream source commit because the former community registry/download endpoints no longer serve the images. Its source is AGPLv3; EspoCRM's storage adapter remains S3-compatible. Service versions, source commit and base-image digests are pinned in Compose/Dockerfile. Do not silently upgrade them. See [CHANGELOG.md](CHANGELOG.md) for the NuriVoyage implementation history.

Open http://localhost:8080. Local role credentials are written by `scripts/local credentials` to `.local/test-credentials.md`. The System Administrator username is `admin@nuri.local`; the other six role usernames are in [the UAT checklist](docs/testing/stage-2-human-uat.md). A separate bootstrap maintenance login uses ESPO_ADMIN_USERNAME/ESPO_ADMIN_PASSWORD. Local email capture: http://localhost:8025. MinIO console: http://localhost:9001 (same private sheet). Documents should be accessed through CRM so record permissions apply.

The seven roles and fields/relationships are documented in [Stage 1 design](docs/nurivoyage/stage-1-design.md). [Migration notes](docs/nurivoyage/migrations.md) describe schema v1. Defaults: ZAR base, ZAR/USD/GBP/EUR/SAR/AED, DD/MM/YYYY, configurable APP_TIMEZONE. Rates and all records are synthetic examples. Baseline workflow statuses are manual; posted accounting, computed balances/profitability, frozen commission calculations and automated travel workflows are later scope.

## Daily commands

```sh
scripts/local start               # build, start, reconcile bootstrap and rebuild
scripts/local stop                # compose down; retain data volumes
scripts/local health-check
scripts/local smoke               # synthetic integration tests, restarts and restore; brief downtime
scripts/local smoke-stage4        # focused Stage 4 enquiry checks
scripts/local smoke-stage5        # focused Stage 5 traveller/document checks
scripts/local smoke-stage6        # focused Stage 6 quote/version checks
scripts/local smoke-stage7        # focused Stage 7 traveller-photo checks
scripts/local backup              # backups/<UTC timestamp>, private permissions
scripts/local restore backups/<timestamp>  # replaces local DB/runtime/documents/email with snapshot
scripts/local bootstrap           # reconcile local defaults, roles/users; no reseed of existing data
scripts/local reset-passwords     # apply current DEV_USER_PASSWORD to seven role users
scripts/local credentials         # regenerate private local credential sheet
scripts/local reset-local         # destructive volume deletion; typed confirmation required
```

Do not run bootstrap, smoke, backups or restores concurrently. Take a backup before resetting. Restore intentionally replaces local data; use only this project's snapshots and matching checkout/.env. Backups include SQL plus Espo data, MinIO and Mailpit files, with checksums. Writers are stopped during snapshots/restores and restarted in a finally block. No automatic destructive cleanup is performed by start/stop. Backup files include runtime secrets, stay local, and must never be committed. `.env` and tracked customisation code are preserved separately; snapshots do not change the Git checkout.

Docker named volumes persist MariaDB, Espo runtime/config/upload staging, MinIO objects and Mailpit. Supported `custom/` and `client/custom/` paths are bind-mounted from Git and survive `compose down`. Administration changes to supported custom metadata/layouts appear in this checkout; review and commit intentionally. No edits inside containers are required. Rebuild after changing metadata; `scripts/local bootstrap` performs it. Reserved future infrastructure is under infrastructure/terraform and contains no resources.

By default all published ports bind to 127.0.0.1. MariaDB/SMTP are not published. `DOCKER_SUBNET` defaults to 10.231.0.0/24 to avoid exhausted Docker Desktop address pools on this Mac; choose another free private /24 in `.env` if it conflicts. See UAT for optional temporary LAN configuration. This is a local development setup, not production hardening.

## Tests and human acceptance

Run `scripts/local smoke` after starting. It checks Compose/container health, page/API login, MariaDB, customer/contact creation and restart persistence, private MinIO upload/download/restart/delete, Espo-to-Mailpit delivery, scheduled jobs, WebSocket handshake, snapshot validity, destructive change/restore recovery, currencies and seven-role API boundaries. It updates [the smoke report](docs/testing/stage-2-smoke-test.md) with actual evidence. No password values are included.

Then follow the [exact 20-step human UAT checklist](docs/testing/stage-2-human-uat.md). Human UAT is pending until a human completes and signs it; leave the local stack running. A PR can be opened after automated smoke tests pass; merge is separate.

## Logs and troubleshooting

```sh
docker compose ps
docker compose logs -f                    # all container stdout/stderr
docker compose logs -f crm                # Apache/PHP process messages
docker compose exec crm sh -c 'tail -f data/logs/*.log' # Espo/PHP application exceptions
docker compose logs -f db                 # MariaDB startup/connection errors
docker compose logs -f daemon             # daemon/scheduler process errors
docker compose exec crm php bin/command app-check
docker compose logs -f websocket
docker compose logs -f minio minio-init    # object store / bucket bootstrap
docker compose logs -f mailpit            # SMTP capture; inspect http://localhost:8025
```

A failed startup is not a successful install. Inspect logs, fix the error, rerun start and smoke. Health checks do not replace role/API tests. If document uploads initially stage in Espo data/upload, wait for the daemon's move job and inspect native Attachment.storage; small API uploads use MinIO directly. Do not use real passports. Delete synthetic files through CRM; do not alter the bucket behind it during normal use.

Official references: [Espo Docker installation](https://docs.espocrm.com/administration/docker/installation/), [file storage](https://docs.espocrm.com/administration/file-storage/), [MinIO pinned source release](https://github.com/minio/minio/tree/9e49d5e7a648f00e26f2246f4dc28e6b07f8c84a).

---

## EspoCRM

[![PHPStan level 8](https://img.shields.io/badge/PHPStan-level%208-brightgreen)](#espocrm)

[EspoCRM](https://www.espocrm.com) is a free, open-source CRM platform designed to help organizations build and maintain strong customer relationships.
It provides a wide range of tools to store, organize, and manage leads, contacts, sales opportunities, marketing campaigns,
support cases, and more – all business information in a simple and intuitive interface.

![Screenshot](https://github.com/user-attachments/assets/d0806394-3691-43a1-83a5-16ad2e7314e2)


### Architecture

EspoCRM is a web application with a frontend designed as a single-page application and a REST API
backend written in PHP.

### Demo

You can try the CRM on an online [demo](https://www.espocrm.com/demo/).

### Requirements

* PHP 8.3 - 8.5;
* MySQL 8.0 (and later), or MariaDB 10.6 (and later);
* PostgreSQL 15 (and later).

For more information about server configuration, see [this article](https://docs.espocrm.com/administration/server-configuration/).

### Download

[Download](https://www.espocrm.com/download/) the latest release from our website or from GitHub [releases](https://github.com/espocrm/espocrm/releases).

### Release notes

Release notes are available at GitHub [releases](https://github.com/espocrm/espocrm/releases).

### Documentation

See the [documentation](https://docs.espocrm.com) for administrators, users and developers.

### Why EspoCRM?

* Open-source transparency. EspoCRM's source code is open and accessible, so anyone can inspect it and see how data is being managed within the CRM.
* Customization freedom. You can develop features, create custom entities, fields, relationships, buttons to make the system fit your specific needs. EspoCRM is more than a CRM – it's a platform for building custom business applications.
* Clean user interface. EspoCRM offers an uncluttered, minimalist, and fast user interface, which is easy to navigate and has a short learning curve.
* Straightforward REST API. It can be easily integrated with other applications using a REST API.

### Who is EspoCRM for?

* From startups, small & medium-sized businesses to larger organizations. A flexible, fully customizable solution that scales with your needs.
* Developers & tech enthusiasts. You can extend functionalities, build extensions, and create custom integrations.
* Anyone seeking a free or on-premise CRM.

### Installing stable version

See installation instructions:

* [Manual installation](https://docs.espocrm.com/administration/installation/)
* [Installation by script](https://docs.espocrm.com/administration/installation-by-script/)
* [Installation with Docker](https://docs.espocrm.com/administration/docker/installation/)
* [Installation with Traefik](https://docs.espocrm.com/administration/docker/traefik/)

### Bug reporting

Create a [GitHub issue](https://github.com/espocrm/espocrm/issues/new/choose) or post on our [forum](https://forum.espocrm.com/forum/bug-reports).

### Development

See the [developer documentation](https://docs.espocrm.com/development/).

We highly recommend using an IDE for development. The backend codebase adheres to SOLID principles, utilizes interfaces, static typing and generics. We recommend to start learning EspoCRM from the Dependency Injection article in the documentation.

Metadata plays an integral role in the EspoCRM application. All possible parameters are described with a JSON Schema, meaning you will have autocompletion in the IDE. You can also find the full metadata reference in the documentation.

The frontend is an SPA built on a custom framework. It utilizes nested views and service DI, with the core partially written in TypeScript. Developers primarily work with existing form and field view implementations.

### Community & Support

If you have a question regarding some features, need help or customizations, want to get in touch with other EspoCRM users, or add a feature request, please use our [community forum](https://forum.espocrm.com/). We believe that using the forum to ask for help and share experience allows everyone in the community to contribute and use this knowledge later.

### License

EspoCRM is an open-source project licensed under [GNU AGPLv3](https://raw.githubusercontent.com/espocrm/espocrm/master/LICENSE.txt).

### Contributing

Before we can merge your pull request, you need to accept our CLA [here](https://github.com/espocrm/cla). See the [contributing guidelines](https://github.com/espocrm/espocrm/blob/master/.github/CONTRIBUTING.md).

Branches:

* *fix* – upcoming maintenance release; minor fixes should be pushed to this branch;
* *master* – develop branch; new features should be pushed to this branch;
* *stable* – last stable release.

### Language

If you want to improve existing translation or add a language that is not available yet, you can contribute on our [POEditor](https://poeditor.com/join/project/gLDKZtUF4i) project. See instructions [here](https://www.espocrm.com/blog/how-to-use-poeditor-to-translate-espocrm/). It may be reasonable to let us know about your intention to join the POEditor project by posting on our forum or via the contact form on our website.

Changes on POEditor are usually merged to the GitHub repository before minor releases.

## Stage 3 branding and review

The Stage 3 branch builds on the approved Stage 1–2 commit, with original UTNT logo, plane favicon, NuriVoyage custom theme, #C2F9FF page canvases, royal-blue controls/nav and gold accents/browser theme hint. [Architecture and limits](docs/nurivoyage/stage-3-branding.md), [brand assets](branding/README.md), [Stage 3 smoke report](docs/testing/stage-3-smoke-test.md) and [exact human UAT checklist](docs/testing/stage-3-human-uat.md).

Use `scripts/local bootstrap` after branding source edits to publish assets, reconcile supported config/templates and rebuild metadata. Use `scripts/local smoke-stage3` for all Stage 2 regressions plus Stage 3 integration checks. Browser viewport testing is separate; see tests/nurivoyage/stage-3-browser.md and its dated evidence. Stage 2 and Stage 3 have been accepted by the user; Stage 4 remains separate and unmerged until its own acceptance. Source assets are under branding/; no core Espo files are edited. PDF layouts are specifications/static previews until native financial functionality is installed.

## Stage 4 leads and enquiries

Stage 4 extends the existing `NvEnquiry` foundation with operational source, contact, destination, service, budget, follow-up and lost-reason fields. Run `scripts/local bootstrap` to apply metadata, `scripts/local smoke-stage4` for the focused checks, and `docs/testing/stage-4-human-uat.md` for localhost acceptance. Stage 4 is accepted.

## Stage 5 travellers and documents

Stage 5 adds passport identity fields to travellers and verification metadata to private travel documents. Run `scripts/local smoke-stage5` for focused checks and follow [the Stage 5 UAT checklist](docs/testing/stage-5-human-uat.md). Stage 5 is accepted.

## Stage 6 quotes and sales pipeline

Stage 6 adds quote numbers, option names, sent and accepted timestamps, lost reasons and the `v10.0.10.0` marker on the login and application pages. Run `scripts/local bootstrap`, `scripts/local smoke-stage6` and follow [the Stage 6 UAT checklist](docs/testing/stage-6-human-uat.md). Stage 6 remains separate and unmerged until accepted.

## Stage 7 travellers and passport photos

Stage 7 delivers the planned bookings and itineraries foundation, adds a private passport photo attachment to the traveller detail page and advances the displayed application version to `v10.0.10.0.s7`. **Sales → Travellers → Create Traveller** adds a person; enter a Customer Number in the Customer selector to link the person to a customer. Alternatively, open a Customer, use **Group Travellers → +** to create a traveller with that customer prefilled, or use **Group Travellers → ⋮ → Select** and search by Traveller Number to link an existing person. Customer and Traveller numbers appear on their pages and lists. Unlinking a group member also removes their booking link for that customer. Open an itinerary and use **City Stops → +** to enter the first two cities, then add as many more as needed. Each stop shows arrival/departure dates, its incoming Car/Bus/Plane/Train transfer and cost. Open a city stop to add one or more hotels, each with check-in/out dates and cost; the itinerary also shows all hotels by city. Transfers and sightseeing have separate related-record panels. A repeatable demonstration fixture is available with `scripts/local seed-stage7-demo`: [synthetic Al Noor customer, number 29](http://localhost:8080/#Account/view/6ad3415bbf5bbc925) and [four-city itinerary](http://localhost:8080/#NvBooking/view/6ad3415c364483e5e). Use only synthetic itinerary data and head-and-shoulders images. Run `scripts/local bootstrap`, `scripts/local smoke-stage7` and follow [the Stage 7 UAT checklist](docs/testing/stage-7-human-uat.md). Stage 7 remains separate and unmerged until accepted.

For a family or group booking, the Customer is the billing/customer account. The Booking has one Lead Traveller, while every other person is a separate Traveller record linked to the same Booking and Group Reference. On a Booking, use **Travellers → +** to create a new member with the Booking prefilled, or **Travellers → ⋮ → Select** to attach an existing Traveller by Traveller Number; the member then appears in the Booking's traveller manifest. The Quote links to the Customer and Booking; the Traveller records provide the passenger manifest and each can have its own passport photo and documents.

## Stage 8 supplier and product catalogue

Stage 8 adds supplier contacts and reusable airline, hotel, transfer, visa, package and activity products. Products include supplier and selling rates, destination, supplier product code, validity dates and active status. Bulk airline and hotel catalogue rows can be loaded from CSV with `scripts/local import-catalogue FILE.csv`; required columns are `supplierName,supplierCategory,productName,productType,destination,supplierCost,sellingPrice`, with optional supplier contact, code, currency and validity columns. Use `NURIVOYAGE_DRY_RUN=1` to validate without writing. Run `scripts/local smoke-stage8` for focused checks.

## Stage 9 procurement and purchase orders

Stage 9 adds purchase-order numbers, supplier references, request and confirmation timestamps, due dates, amounts and the supplier confirmation lifecycle. Run `scripts/local smoke-stage9` for focused checks.

## Stage 10 invoices payments and balances

Stage 10 adds invoice numbers, paid and balance amounts, customer deposits, payments, refunds and invoice allocation references. Run `scripts/local smoke-stage10` for focused checks.

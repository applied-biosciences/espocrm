# NURIVOYAGE STAGE 3 SMOKE TEST

Run UTC: 2026-10-17T04:19:52.485604+00:00

Command: `scripts/local smoke-stage3`

| Automated integration check | Result | Evidence |
|---|---|---|
| Local-only SMTP guard | PASS | System Group Email Account is Mailpit:1025 only; IMAP and upstream relay disabled |
| Full Stage 2 regression | PASS | ALL 18 CHECKS PASSED. Human UAT is pending. |
| Six service health | PASS | PASS db: running/healthy PASS crm: running/healthy PASS daemon: running/healthy PASS websocket: running/healthy PASS minio: running/healthy PASS mailpit: running/healthy PASS http://localhost:8080/ PASS http://localhost:9000/minio/health/live PASS http://localhost:8025/readyz |
| Brand identity and restart persistence | PASS | Title, theme, custom login, logo, favicon and legal notice persist after stack/MinIO restart and restore |
| Browser assets | PASS | 13 custom/base assets return HTTP 200; supplied PNGs preserved byte-for-byte |
| Navigation configuration | PASS | Native ACL-filtered groups; all 19 real custom modules; Customers label; no fake dashboard/report links |
| Branded local email | PASS | 3 branded templates sent through Espo to Mailpit, with HTML and plain-text alternatives |
| PDF branding foundation | PASS | Three A4 print-layout specifications/previews; explicit legal/contact placeholders; no duplicate invoice/PO engine |
| Palette contrast | PASS | Text contrast ratios 14.39, 10.87, 5.94, 7.44 :1; gold remains an accent; visible keyboard focus and zoom enabled |
| Logs and custom assets | PASS | No new fatal container errors or custom-asset HTTP 404s in the review window |

## Browser automation evidence

Captured through desktop CUA on 2026-10-17T04:21:05.259Z. The CLI integration run above and browser automation are separate. See [browser procedure](../../tests/nurivoyage/stage-3-browser.md).

| Screen | Viewport | Result |
|---|---|---|
| bookings | 1440×900 | PASS |
| bookings | 1280×800 | PASS |
| bookings | 768×1024 | PASS |
| bookings | 390×844 | PASS |
| mobile navigation | 390×844 | PASS |
| booking form | 390×844 | PASS |
| login | 1440×900 | PASS |
| login | 1280×800 | PASS |
| login | 768×1024 | PASS |
| login | 390×844 | PASS |
| role navigation sales | 1280×800 | PASS |
| role navigation hybrid | 1280×800 | PASS |
| role navigation finance | 1280×800 | PASS |
| role navigation manager | 1280×800 | PASS |
| login after restart and restore | 1440×900 | PASS |
| bookings after restart and restore | 1440×900 | PASS |
| booking form after layout polish | 390×844 | PASS |
| PDF layout foundation preview | 1440×900 | PASS |

Browser warning: four native `Autobahn not connected` messages appeared during rapid role login/logout. No new message appeared during the subsequent normal administrator logout. The native WebSocket service/handshake passed; this non-blocking upstream race is retained for human review. There were no custom-asset 404s or custom JavaScript errors.

Additional targeted checks: all three static PDF-layout previews return HTTP 200 with gold theme metadata and plane favicon; the final mobile booking form contains exactly one Assigned User label.

Stage 3 human UAT is **PENDING**. [Exact checklist](stage-3-human-uat.md). No AWS deployment, production data or external email delivery.

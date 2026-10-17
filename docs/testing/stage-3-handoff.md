# Stage 3 local handoff

Implementation branch: `codex/nurivoyage-stage-3`. Approved base: `24a945c5a31a03981303e75dd25e5ccb220f6882`. Stage 3 is prepared as a separate review against the Stage 1–2 branch; master is not changed or merged. Obtain the implementation SHA from the final handoff or `git log -1 --format=%H`.

CRM http://localhost:8080 ; Mailpit http://localhost:8025 ; MinIO http://localhost:9001. The six persistent services remain healthy/running. Role logins/passwords and reset method remain in ignored `.local/test-credentials.md` (`scripts/local credentials` regenerates the sheet without resetting passwords).

Implemented: supplied company logo unchanged, exact #C2F9FF web page canvases, royal blue/navy controls and navigation, restrained gold accents, gold browser theme hint, plane.png favicon, branded native login/header, grouped role-aware navigation, Customers label, appropriate module icons, responsive styling, focus/zoom improvements and three local email templates. PDF design/print foundations are static previews only because Sales Pack is absent; no duplicate engine is built. All changes use supported custom/config/metadata paths.

Validation: all 18 Stage 2 regressions PASS; all 10 Stage 3 integration checks PASS; recorded browser checks cover four viewport sizes, mobile navigation/form usability, four role menus and branding after restart/restore. Three branded HTML/plain-text messages were captured only in Mailpit. Original supplied PNG hashes match their published copies. No core file edits, AWS deployment, real customer data or external email delivery.

Review [smoke results](stage-3-smoke-test.md), [dated browser evidence](stage-3-browser-evidence.json), [exact Stage 3 human UAT](stage-3-human-uat.md), [changed files](stage-3-changed-files.md), [architecture and known limitations](../nurivoyage/stage-3-branding.md), and screenshots/.

Known non-blocking observation: four native “Autobahn not connected” console messages occurred during rapid automated role-login/logout. No new message appeared during subsequent normal administrator logout; the WebSocket service/handshake and workflows pass. This likely upstream connect/disconnect race is retained in the evidence and is not patched in core. Browser theme-color is a hint; tab-strip rendering depends on browser/platform. Native navigation collapses below 1320px and lists may use internal scrolling. Full financial workflows, reporting and generated PDFs remain later scope.

Stage 2 was human-accepted by the user on 17 October 2026. **Stage 3 human UAT is pending. Do not merge Stage 3 until explicitly accepted.** The local stack and browser login page are left available for review.

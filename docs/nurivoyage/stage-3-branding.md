# Stage 3 architecture and scope

Branch `codex/nurivoyage-stage-3` starts at approved `24a945c5a31a03981303e75dd25e5ccb220f6882`. The task specification is preserved at docs/tasks/NURIVOYAGE_STAGE_3.md. The user's current palette and supplied assets override the task's generic light-grey/placeholder suggestions. Stage 2 human acceptance is recorded from the user's “passed” message on 17 October 2026; Stage 3 human UAT remains pending.

## Upgrade-safe layers

1. `custom/.../metadata/themes/NuriVoyage.json` selects a custom stylesheet/iframe stylesheet, logo, chart palette and native side navigation. It imports the pinned upstream Light CSS; core CSS is not copied or modified. CSS tokens cover controls, panels, tables, modals, links, state text and focus. All web page canvases use #C2F9FF; white is reserved for cards/controls and print paper. User themes are disabled in this branded local baseline to keep the requested appearance consistent.
2. `app/client.json` appends a presentation-only head script and configures the original plane.png favicon. The head script sets gold theme-color and restores browser zoom. It does not change authentication or permissions. Browser chrome colouring is a platform-controlled hint, not a guarantee for every desktop tab strip.
3. `loginView` is a supported configuration setting exposed as a read-only global view identifier through `app/config.json`. The custom LoginView extends native LoginView. Native form IDs, SSO/fallback hooks, password recovery, login event handling and second-step delegation remain in the pinned native implementation. The template is a supported custom template derived from the v10.0.10 native controls. Review these bindings when upgrading; no alternate authentication engine is added. Password-show receives a keyboard label/activation handler.
4. `clientDefs/App.json` selects a native NavbarView subclass. It adds the NuriVoyage text identity, logo alt text and accessible labels for collapsed navigation. It retains native menu construction, ACL filtering, preferences, dropdowns and responsive behaviour. `navigation.json` groups only existing modules. Management Dashboard/Reports remain planned, with no placeholder routes. Account's display label becomes Customer through custom translations. Icon choices and duplicate Assigned User removal in the custom main detail layouts are presentation changes; native side assignment panels remain.
5. Bootstrap reconciles the theme, descriptor, sender display name, groups and three native EmailTemplate records. The original seven-role access rules are retained; the Management role gains the existing EmailTemplate scope so it can review branding templates. No Sales/Hybrid cost, commission or creditor grants are expanded. SQL schema remains v1 with no new business entities/fields.
6. Original user-provided PNGs live under branding/ and are copied unchanged into client/custom/branding by publish-branding.py. HTML email sources are mirrored into the existing read-only scripts mount. Static PDF-layout preview copies are generated from the stored specifications; no financial or PDF engine is added. The legal EspoCRM footer remains visible.

## Documents and email

See branding/pdf/README.md for A4 template fields and future approved renderer/record mapping. Sales Pack is not installed, so actual financial PDF generation is outside this stage. The static previews contain no real data and clearly identify placeholders. Print CSS is white; web preview canvas is cyan.

See branding/email/README.md for three native templates, placeholder convention, HTML and plain-text sources. The integration test supplies synthetic values and checks HTML/Text in Mailpit. Local bootstrap refuses SMTP_HOST other than mailpit or SMTP_PORT other than 1025. The existing system Group Email Account has IMAP disabled and Mailpit has no external relay. No external email is sent.

## Testing and persistence

`scripts/local smoke-stage3` first verifies local-only SMTP, runs all 18 Stage 2 API/service/backup/restore tests, then checks identity, restart persistence, every published asset, source-image byte equality, grouped navigation, branded email capture, PDF foundations, contrast and logs. Full API cost/commission regression remains unchanged. Stage 3 browser checks are performed separately through CUA at 1440×900, 1280×800, 768×1024 and 390×844, including login/form controls, no page overflow, native mobile navigation and four role menus. The dated evidence and screenshots are attached to the report; the CLI does not claim to rerun a browser itself.

No reset of human-created local data is needed for Stage 3. Named volumes/config remain persisted; the existing integration test alters and restores only its own synthetic fixtures using a full snapshot. Brand assets and metadata are Git-backed bind mounts, and bootstrap re-applies brand defaults after a fresh install. No AWS change, real customer data, native mobile application, portal or future financial workflow is implemented.

## Known limits for human review

- Stage 3 human and actual LAN-device UAT are pending; automated viewport testing is not human acceptance.
- Four native “Autobahn not connected” console messages were captured during the rapid role-login/logout loop. The native WebSocket manager attempts close/unsubscribe while a connection may still be opening (likely source of the race); the subsequent normal admin logout produced no new message. The service/handshake and all workflows tested pass. This is retained as a non-blocking upstream warning rather than patched in core.
- Native page titles can show the current module name after login; the root/login title is NuriVoyage and navigation/favicon retain the identity.
- The browser decides whether theme-color changes its chrome/tab strip. Some browsers ignore it or cache favicons; hard refresh if needed.
- Native navigation initially collapses below 1320px; this behaviour is retained with readable labels. Wide lists can use internal horizontal scroll, preserving the no-page-overflow requirement.
- Existing dashboard panels are styled; no Stage 13 management dashboard or fake totals are created.
- No generated PDF claims: review the stored design foundation until appropriate native functionality is integrated.
- Technical administrators retain Espo's inherent ACL bypass; commercial roles retain the Stage 1 boundaries.

Official extension references used: https://docs.espocrm.com/development/custom-views/ and https://docs.espocrm.com/development/metadata/. All extensions must be reviewed with the v10.0.10 native selectors/theme tokens on a future deliberate upgrade.

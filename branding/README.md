# NuriVoyage Stage 3 brand system

Application: NuriVoyage. Descriptor: Travel Management Platform. Company: Nuri's Travel. The supplied UTNT company logo is used unchanged; no new final logo is invented. Original plane artwork is retained byte-for-byte as plane.png.

## Palette

- Web page canvas: **#C2F9FF** everywhere, overriding the task's #F6F8FB suggestion.
- Primary navigation, links and buttons: royal blue **#123B7A**.
- Body text and headings: deep navy **#0B1F3A**.
- Accents / browser theme-colour hint: gold **#C9A227**.
- Selected decorative/icon accents: soft gold **#E7D59A**.
- Content cards, inputs and printed PDF paper: white **#FFFFFF** for readability.

Gold is not ordinary body text and is not the sole active/error indicator. The active navigation item has a contrasting navy surface, gold edge and native current-item styling. Native status text remains present. Keyboard focus is visible. The browser zoom restriction in the upstream viewport tag is removed by the custom head script.

## Files and publication

`logo/utnt-logo.png` and `favicon/plane.png` are the original supplied PNGs. `email/` contains HTML plus plain-text foundation templates. `pdf/` contains A4 print-layout HTML specifications, not a transaction/PDF engine. No registration, VAT, banking or address details are invented.

`scripts/nurivoyage/publish-branding.py` publishes unchanged logo/favicon copies to `client/custom/branding`, static PDF-layout previews below `client/custom/branding/pdf`, and mirrors email HTML into the existing scripts mount for bootstrap. `scripts/local start`, `bootstrap` and `reset-passwords` run publication. Published assets are tracked so a checkout already contains everything needed by the running application.

The custom NuriVoyage metadata theme imports Espo's pinned Light CSS and overrides design tokens plus scoped presentation rules. A supported custom LoginView subclass retains native authentication logic; its template preserves the native controls/SSO hooks. The custom NavbarView subclass retains native navigation and ACL filtering and adds identity/accessible labels. The legal EspoCRM footer remains. No core files or bundles are edited.

`meta[name=theme-color]` is set to gold. This is a browser hint: browser chrome/tab-strip colouring is controlled by the user's browser/platform and cannot be forced uniformly. The plane favicon is configured through app.client metadata. A normal reload/hard refresh may be needed to clear a previously cached favicon or frontend asset.

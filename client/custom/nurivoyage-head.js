/* Loaded through app.client metadata. Presentation only; no authentication or ACL changes. */
(() => {
    const version = 'v10.0.10.0.s18';
    const addVersionBadge = () => {
        if (document.querySelector('.nuri-version-badge')) return;
        const badge = document.createElement('span');
        badge.className = 'nuri-version-badge';
        badge.textContent = version;
        badge.setAttribute('aria-label', `NuriVoyage version ${version}`);
        document.body.append(badge);
    };
    if (document.body) addVersionBadge();
    else document.addEventListener('DOMContentLoaded', addVersionBadge, {once: true});
    let theme = document.querySelector('meta[name="theme-color"]');
    if (!theme) {
        theme = document.createElement('meta');
        theme.name = 'theme-color';
        document.head.append(theme);
    }
    theme.content = '#C9A227';
    // Restore browser zoom support without changing upstream HTML.
    const viewport = document.querySelector('meta[name="viewport"]');
    if (viewport) viewport.content = 'width=device-width, initial-scale=1';
    else document.addEventListener('DOMContentLoaded', () => {
        const meta = document.querySelector('meta[name="viewport"]');
        if (meta) meta.content = 'width=device-width, initial-scale=1';
    }, {once: true});
})();

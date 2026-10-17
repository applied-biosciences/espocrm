/* Loaded through app.client metadata. Presentation only; no authentication or ACL changes. */
(() => {
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

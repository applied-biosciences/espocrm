define('custom:views/nurivoyage/login', ['views/login'], LoginView => {
    return class extends LoginView {
        template = 'custom:nurivoyage/login';
        afterRender() {
            super.afterRender();
            const toggle = this.element.querySelector('[data-action="toggleShowPassword"]');
            if (toggle) {
                toggle.setAttribute('aria-label', 'Show or hide password');
                toggle.setAttribute('tabindex', '0');
                toggle.addEventListener('keydown', e => {
                    if (e.key === 'Enter' || e.key === ' ') { e.preventDefault(); toggle.click(); }
                });
            }
        }
    };
});

define('custom:views/nurivoyage/navbar', ['views/site/navbar'], NavbarView => {
    return class extends NavbarView {
        afterRender() {
            super.afterRender();
            this.element.querySelectorAll('.tabs a').forEach(link => {
                const text = link.querySelector('.full-label')?.textContent?.trim();
                if (text) { link.setAttribute('aria-label', text); link.setAttribute('title', text); }
            });
            this.element.querySelectorAll('.navbar-toggle,.side-menu-button').forEach(button => {
                button.setAttribute('aria-label', 'Toggle navigation');
                button.setAttribute('title', 'Toggle navigation');
            });
            const brand = this.element.querySelector('.navbar-brand');
            if (brand && !brand.querySelector('.nuri-app-name')) {
                const label = document.createElement('span');
                label.className = 'nuri-app-name';
                label.textContent = 'NuriVoyage';
                brand.append(label);
                brand.setAttribute('aria-label', 'NuriVoyage home');
                const image = brand.querySelector('img');
                if (image) image.alt = "Umra Tours and Nuri's Travels";
            }
            if (brand && !brand.querySelector('.nuri-version')) {
                const version = document.createElement('small');
                version.className = 'nuri-version';
                version.textContent = 'v10.0.10.0.s13';
                brand.append(version);
            }
        }
    };
});

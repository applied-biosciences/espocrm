define('custom:views/nurivoyage/fx', ['view'], View => class extends View {
    template = 'custom:nurivoyage/fx';
    async afterRender() {
        this.rates = null;
        this.activeCurrency = 'ZAR';
        this.element.querySelector('[data-action="refreshRates"]').addEventListener('click', () => this.refreshRates());
        this.element.querySelectorAll('input[data-currency]').forEach(input => input.addEventListener('input', () => this.convert(input)));
        await this.refreshRates();
    }
    convert(input) {
        if (!this.rates || input.value === '' || !Number.isFinite(Number(input.value))) return;
        this.activeCurrency = input.dataset.currency;
        const usd = Number(input.value) / this.rates[input.dataset.currency];
        this.element.querySelectorAll('input[data-currency]').forEach(other => {
            if (other !== input) other.value = (usd * this.rates[other.dataset.currency]).toFixed(2);
        });
    }
    async refreshRates() {
        const button = this.element.querySelector('button');
        const status = this.element.querySelector('[role="status"]');
        button.disabled = true;
        status.textContent = 'Updating rates…';
        try {
            const response = await fetch('https://api.frankfurter.dev/v2/rates?base=USD&quotes=GBP,ZAR,SAR', {signal: AbortSignal.timeout(20000)});
            if (!response.ok) throw new Error('Provider returned HTTP ' + response.status);
            const rows = await response.json();
            const rates = {USD: 1};
            rows.forEach(row => { if (['GBP', 'ZAR', 'SAR'].includes(row.quote) && Number(row.rate) > 0) rates[row.quote] = Number(row.rate); });
            if (!['USD','GBP','ZAR','SAR'].every(code => rates[code])) throw new Error('Provider response is missing a required currency');
            this.rates = rates;
            status.textContent = 'Frankfurter reference rates: ' + rows.map(row => row.date).sort()[0] + ' · Refreshed ' + new Date().toLocaleString();
            this.element.querySelectorAll('input').forEach(input => input.disabled = false);
            this.convert(this.element.querySelector('[data-currency="' + this.activeCurrency + '"]'));
        } catch (error) {
            status.textContent = 'Rates could not be updated: ' + error.message + (this.rates ? '. Previous rates retained.' : '. Click Update rates to retry.');
        } finally { button.disabled = false; }
    }
});

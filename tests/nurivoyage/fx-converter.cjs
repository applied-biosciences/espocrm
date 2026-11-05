// Exercise the shipped view logic, including provider failures and refresh preservation.
const assert = require('node:assert/strict');
const fs = require('node:fs');
let Fx;
global.define = (_name, _deps, factory) => { Fx = factory(class {}); };
eval(fs.readFileSync('client/custom/src/views/nurivoyage/fx.js', 'utf8'));
const fields = ['USD','GBP','ZAR','SAR'].map(currency => ({dataset:{currency},value:currency==='ZAR'?'1000':'',disabled:true}));
const button = {disabled:false};
const status = {};
const view = new Fx();
view.element = {
 querySelector(selector) { if(selector==='button') return button; if(selector==='[role="status"]') return status; return fields.find(f=>selector.includes('"'+f.dataset.currency+'"')); },
 querySelectorAll() {return fields;}
};
view.activeCurrency='ZAR';
const rates={USD:1,GBP:0.75,ZAR:18,SAR:3.75};
global.fetch=async()=>({ok:true,json:async()=>Object.entries(rates).filter(([c])=>c!=='USD').map(([quote,rate])=>({quote,rate,date:'2026-10-17'}))});
(async()=>{
 await view.refreshRates();
 for(const source of fields){source.value='100';view.convert(source);for(const target of fields){assert.ok(Math.abs(Number(target.value)-100/rates[source.dataset.currency]*rates[target.dataset.currency])<0.006);}}
 fields[0].value='200';view.convert(fields[0]);await view.refreshRates();assert.equal(fields[0].value,'200');
 global.fetch=async()=>{throw Error('offline')};await view.refreshRates();assert.match(status.textContent,/Previous rates retained/);assert.equal(button.disabled,false);
 console.log('PASS shipped converter: all input currencies, refresh preservation and provider failure');
})().catch(e=>{console.error(e);process.exit(1)});

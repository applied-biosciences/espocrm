#!/usr/bin/env python3
"""Stage 6 authenticated localhost checks for quotes and version branding."""
import pathlib, urllib.request, uuid
ROOT = pathlib.Path(__file__).resolve().parents[2]
p = ROOT / 'tests/nurivoyage/smoke.py'
source = p.read_text(); ns = {'__file__': str(p)}
exec(source[:source.index('try:\n    stamp=')], ns)
api = ns['api']
fields = api('Metadata')['entityDefs']['NvQuote']['fields']
required = ['quoteNumber','optionName','sentAt','acceptedAt','lostReason']
assert all(name in fields for name in required)
html = urllib.request.urlopen('http://localhost:8080/').read().decode()
assert 'v10.0.10.0' in html or 'nurivoyage-head.js' in html
print('PASS Stage 6 metadata and version asset')
stamp = uuid.uuid4().hex[:8]
quote = api('NvQuote', 'POST', {
    'name':'Stage 6 Synthetic Quote '+stamp, 'quoteNumber':'NV-Q-'+stamp,
    'optionName':'Family Umrah Standard', 'status':'Draft', 'sellingPrice':25000,
    'sellingPriceCurrency':'ZAR', 'validUntil':'2026-11-30'
}, user='sales')
api('NvQuote/'+quote['id'], 'PUT', {'status':'Sent','sentAt':'2026-10-20 10:00:00'}, user='sales')
api('NvQuote/'+quote['id'], 'PUT', {'status':'Accepted','acceptedAt':'2026-10-21 10:00:00'}, user='sales')
detail = api('NvQuote/'+quote['id'], user='sales')
assert detail['quoteNumber'] == 'NV-Q-'+stamp and detail['status'] == 'Accepted'
print('PASS Stage 6 quote lifecycle: Draft to Sent to Accepted persisted')

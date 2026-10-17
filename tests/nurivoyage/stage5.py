#!/usr/bin/env python3
"""Stage 5 authenticated localhost checks for travellers and documents."""
import base64, pathlib, uuid
ROOT = pathlib.Path(__file__).resolve().parents[2]
p = ROOT / 'tests/nurivoyage/smoke.py'
source = p.read_text(); ns = {'__file__': str(p)}
exec(source[:source.index('try:\n    stamp=')], ns)
api = ns['api']

fields = api('Metadata')['entityDefs']
required_traveller = ['passportNumber','passportCountry','passportIssueDate','passportExpiryDate']
required_document = ['documentNumber','countryOfIssue','issueDate','verificationStatus','verifiedAt','verifiedBy']
assert all(name in fields['NvTraveller']['fields'] for name in required_traveller)
assert all(name in fields['NvTravelDocument']['fields'] for name in required_document)
print('PASS Stage 5 metadata: traveller and document verification fields present')

stamp = uuid.uuid4().hex[:8]
account = api('Account', 'POST', {'name':'Stage 5 Synthetic Customer '+stamp}, user='admin')
traveller = api('NvTraveller', 'POST', {
    'name':'Stage 5 Synthetic Traveller '+stamp, 'customerId':account['id'],
    'nationality':'South African', 'passportNumber':'SYNTH-'+stamp,
    'passportCountry':'South Africa', 'passportIssueDate':'2024-01-10',
    'passportExpiryDate':'2034-01-09'
}, user='operations')
document = api('NvTravelDocument', 'POST', {
    'name':'Stage 5 Synthetic Passport '+stamp, 'travellerId':traveller['id'],
    'documentType':'Synthetic Passport', 'documentNumber':'DOC-'+stamp,
    'countryOfIssue':'South Africa', 'issueDate':'2024-01-10',
    'expiryDate':'2034-01-09', 'verificationStatus':'Pending'
}, user='operations')
api('NvTravelDocument/'+document['id'], 'PUT', {'verificationStatus':'Verified'}, user='operations')
detail = api('NvTravelDocument/'+document['id'], user='operations')
assert detail['verificationStatus'] == 'Verified'
try:
    api('NvTravelDocument/'+document['id'], user='sales', expected=(403,404))
except AssertionError:
    raise
print('PASS Stage 5 lifecycle: Operations created and verified a synthetic document; Sales access denied')

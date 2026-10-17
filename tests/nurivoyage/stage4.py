#!/usr/bin/env python3
"""Stage 4 authenticated localhost checks for the leads and enquiries extension."""
import json, pathlib, uuid
ROOT = pathlib.Path(__file__).resolve().parents[2]
p = ROOT / 'tests/nurivoyage/smoke.py'
source = p.read_text(); ns = {'__file__': str(p)}
exec(source[:source.index('try:\n    stamp=')], ns)
api, check = ns['api'], ns['check']

def metadata():
    entity = api('Metadata')['entityDefs']['NvEnquiry']['fields']
    required = ['contact','source','sourceDetail','destination','serviceType','preferredContactMethod','budget','nextFollowUpAt','lostReason']
    assert all(name in entity for name in required), sorted(entity)
    return 'NvEnquiry metadata exposes all Stage 4 fields'
check('Stage 4 metadata', metadata)

def create_and_read():
    stamp = uuid.uuid4().hex[:8]
    record = api('NvEnquiry', 'POST', {
        'name': 'Stage 4 synthetic enquiry ' + stamp,
        'status': 'New Enquiry', 'source': 'Website', 'sourceDetail': 'Local UAT',
        'destination': 'Makkah and Madinah', 'serviceType': 'Umrah',
        'preferredContactMethod': 'Email', 'travellerCount': 2,
        'budget': 25000, 'budgetCurrency': 'ZAR', 'nextFollowUpAt': '2026-10-20 10:00:00'
    }, user='sales')
    detail = api('NvEnquiry/' + record['id'], user='sales')
    assert detail['source'] == 'Website' and detail['serviceType'] == 'Umrah'
    assert detail['destination'] == 'Makkah and Madinah' and detail['budget'] == 25000
    api('NvEnquiry/' + record['id'], 'PUT', {'status':'Lost','lostReason':'No Response'}, user='sales')
    final = api('NvEnquiry/' + record['id'], user='sales')
    assert final['status'] == 'Lost' and final['lostReason'] == 'No Response'
    return 'Sales created, read, updated and terminally closed a synthetic enquiry'
check('Stage 4 enquiry lifecycle', create_and_read)
print('Stage 4 checks passed')

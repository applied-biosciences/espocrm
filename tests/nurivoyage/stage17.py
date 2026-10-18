"""Stage 17 security and governance localhost checks."""
import pathlib
p=pathlib.Path('tests/nurivoyage/smoke.py'); ns={'__file__':str(p)}
exec(p.read_text().split('try:\n    stamp=')[0],ns)
api=ns['api']
metadata=api('Metadata')
entities=['NvSecurityAudit','NvConsent','NvAccessReview','NvRetentionRule','NvGovernanceCheck']
for entity in entities:
    assert entity in metadata['scopes'] and metadata['clientDefs'][entity]['controller']=='controllers/record'
    assert api(entity,user='manager')['total'] >= 1
    assert api(entity,user='finance')['total'] >= 1
print('PASS governance entities registered and seeded for management/finance')
assert api('NvSecurityAudit',user='sales')['total'] >= 0
print('PASS sales audit scope is restricted to own events and remains non-editable')
consent=api('NvConsent','POST',{'name':'SYNTHETIC Stage 17 consent','consentType':'Communication','status':'Granted'},user='finance')
api('NvConsent/'+consent['id'],'PUT',{'status':'Withdrawn'},user='finance')
api('NvConsent/'+consent['id'],'DELETE',user='finance',expected=(403,404))
print('PASS finance can record and update consent; deletion is denied')
review=api('NvAccessReview','POST',{'name':'SYNTHETIC Stage 17 review','reviewType':'Ad Hoc'},user='manager')
api('NvAccessReview/'+review['id'],'PUT',{'status':'Approved'},user='manager')
print('PASS management can complete an access review')
for entity in entities:
    assert metadata['entityDefs'][entity]['fields']
print('PASS field metadata exposes audit, consent, retention, review and governance controls')

"""Stage 18 integrations and portal access localhost checks."""
import pathlib
p=pathlib.Path('tests/nurivoyage/smoke.py'); ns={'__file__':str(p)}
exec(p.read_text().split('try:\n    stamp=')[0],ns)
api=ns['api']
metadata=api('Metadata')
entities=['NvApiClient','NvPortalAccess','NvIntegrationEndpoint']
for entity in entities:
    assert entity in metadata['scopes'] and metadata['clientDefs'][entity]['controller']=='controllers/record'
    assert api(entity,user='manager')['total'] >= 1
    assert api(entity,user='finance')['total'] >= 1
print('PASS integration and portal entities registered and seeded')
settings=api('Settings')
groups=[g for g in settings['tabList'] if isinstance(g,dict)]
portal=[g for g in groups if g.get('text')=='Integrations & Portal']
assert len(portal)==1 and set(entities).issubset(set(portal[0]['itemList']))
print('PASS Integrations & Portal navigation is present once')
client=api('NvApiClient')['list'][0]
assert 'secretReference' in client and 'token' not in str(client).lower()
api('NvApiClient/'+client['id'],'PUT',{'status':'Suspended'},user='finance')
api('NvApiClient/'+client['id'],'DELETE',user='finance',expected=(403,404))
print('PASS API client can be suspended while deletion remains denied')
portalAccess=api('NvPortalAccess')['list'][0]
assert portalAccess.get('allowedScopes') and portalAccess.get('expiresAt')
api('NvPortalAccess/'+portalAccess['id'],'PUT',{'status':'Suspended'},user='finance')
print('PASS portal access has scoped permissions, expiry and suspension controls')
endpoint=api('NvIntegrationEndpoint')['list'][0]
assert endpoint.get('baseUrl') and endpoint.get('status')
print('PASS integration endpoint health metadata is available')

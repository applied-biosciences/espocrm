#!/usr/bin/env python3
"""Focused v10.0.10.01 regression checks for users, PDF output and email links."""
import base64
import json
import pathlib
import urllib.error
import urllib.parse
import urllib.request
import uuid

ROOT = pathlib.Path(__file__).resolve().parents[2]
ENV = dict(line.split('=', 1) for line in (ROOT / '.env').read_text().splitlines()
           if line and not line.startswith('#') and '=' in line)
BASE = 'http://localhost:8080/'
ADMIN = (ENV['ESPO_ADMIN_USERNAME'], ENV['ESPO_ADMIN_PASSWORD'])

def request(path, method='GET', data=None, user=ADMIN, expected=(200, 201)):
    headers = {'Content-Type': 'application/json'}
    if user:
        token = base64.b64encode(f'{user[0]}:{user[1]}'.encode()).decode()
        headers['Authorization'] = 'Basic ' + token
    body = json.dumps(data).encode() if data is not None else None
    req = urllib.request.Request(BASE + path, data=body, headers=headers, method=method)
    try:
        with urllib.request.urlopen(req, timeout=60) as response:
            status, raw = response.status, response.read()
    except urllib.error.HTTPError as error:
        status, raw = error.code, error.read()
    assert status in expected, f'{method} {path}: HTTP {status} {raw[:500]!r}'
    return json.loads(raw) if raw else None

def get(path, user=ADMIN):
    return request(path, user=user)

head = urllib.request.urlopen(BASE + 'client/custom/nurivoyage-head.js', timeout=30).read().decode()
assert 'v10.0.10.01' in head
print('PASS v10.0.10.01 version asset')

app = get('api/v1/App/user')
tab_list = app['settings']['tabList']
management = next(group for group in tab_list if group.get('text') == 'Management Dashboards & Reporting')
workspace = next(group for group in tab_list if group.get('text') == 'Workspace')
user_link = next(item for item in management['itemList'] if (item == 'User') or (isinstance(item, dict) and item.get('url') == '#User'))
assert user_link == 'User' or (user_link.get('type') == 'url' and user_link.get('onlyAdmin') is True)
group_email_link = next(item for item in workspace['itemList'] if isinstance(item, dict) and item.get('url') == '#Admin/groupEmailAccounts')
outbound_email_link = next(item for item in workspace['itemList'] if isinstance(item, dict) and item.get('url') == '#Admin/outboundEmails')
assert group_email_link.get('type') == 'url' and group_email_link.get('onlyAdmin') is True
assert outbound_email_link.get('type') == 'url' and outbound_email_link.get('onlyAdmin') is True
print('PASS Management User link and administrator email-client links')

roles = get('api/v1/Role?maxSize=50')['list']
sales_role = next(role for role in roles if role['name'] == 'Sales Agent')
suffix = uuid.uuid4().hex[:10]
username = f'smoke-release-{suffix}@nuri.local'
password = f'Smoke-{suffix}-one'
changed_password = f'Smoke-{suffix}-two'
created_id = None
try:
    created = request('api/v1/User', 'POST', {
        'userName': username,
        'firstName': 'Smoke',
        'lastName': 'Release',
        'emailAddress': username,
        'phoneNumber': '+27821234571',
        'type': 'regular',
        'isActive': True,
        'password': password,
        'rolesIds': [sales_role['id']],
    })
    created_id = created['id']
    assert created['emailAddress'] == username and created['phoneNumber'] == '+27821234571'
    updated = request(f'api/v1/User/{created_id}', 'PUT', {
        'phoneNumber': '+27821234572',
        'password': changed_password,
        'rolesIds': [sales_role['id']],
    })
    assert updated['phoneNumber'] == '+27821234572'
    logged_in = get('api/v1/App/user', user=(username, changed_password))
    assert logged_in['user']['userName'] == username
    print('PASS admin user create, role assignment, password change and login')
finally:
    if created_id:
        request(f'api/v1/User/{created_id}', 'DELETE', expected=(200, 204))

template_list = get('api/v1/Template?maxSize=100')['list']
records = {
    'NvQuote': 'NuriVoyage Quote PDF',
    'NvCustomerInvoice': 'NuriVoyage Customer Invoice PDF',
    'NvPurchaseOrder': 'NuriVoyage Purchase Order PDF',
}
for entity, template_name in records.items():
    matching = [template for template in template_list if template.get('entityType') == entity and template.get('status') == 'Active']
    assert len(matching) == 1, (entity, matching)
    record = get(f'api/v1/{entity}?maxSize=1')['list'][0]
    query = urllib.parse.urlencode({
        'entryPoint': 'pdf', 'entityType': entity, 'entityId': record['id'], 'templateId': matching[0]['id'],
    })
    req = urllib.request.Request(BASE + '?' + query)
    token = base64.b64encode(f'{ADMIN[0]}:{ADMIN[1]}'.encode()).decode()
    req.add_header('Authorization', 'Basic ' + token)
    with urllib.request.urlopen(req, timeout=60) as response:
        pdf = response.read()
        assert response.status == 200 and response.headers.get('Content-Type') == 'application/pdf'
    assert pdf.startswith(b'%PDF-') and len(pdf) > 1000 and b'/Count 1' in pdf
    print(f'PASS generated PDF: {entity} ({len(pdf)} bytes)')

print('ALL v10.0.10.01 CHECKS PASSED.')

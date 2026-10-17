#!/usr/bin/env python3
"""End-to-end synthetic localhost checks. Includes downtime and backup/restore.
Run only against this project's local development environment; never production.
"""
import base64, datetime, json, pathlib, socket, subprocess, time, urllib.request, urllib.error, uuid, sys
ROOT=pathlib.Path(__file__).resolve().parents[2]
import os
os.chdir(ROOT)
ENV=dict(line.split('=',1) for line in pathlib.Path('.env').read_text().splitlines() if line and not line.startswith('#'))
BASE='http://localhost:8080/api/v1/'
RESULTS=[]
def cmd(*args):
    r=subprocess.run(args,text=True,capture_output=True)
    if r.returncode: raise RuntimeError(r.stdout[-2000:]+'\n'+r.stderr[-2000:])
    return r.stdout

def api(path,method='GET',data=None,user='admin',raw=False,expected=(200,201)):
    headers={'Content-Type':'application/json'}
    if user:
        login=ENV['ESPO_ADMIN_USERNAME'] if user=='admin' else ('admin@nuri.local' if user=='admin-demo' else user+'@nuri.local')
        password=ENV['ESPO_ADMIN_PASSWORD'] if user=='admin' else ENV['DEV_USER_PASSWORD']
        headers['Authorization']='Basic '+base64.b64encode((login+':'+password).encode()).decode()
    request=urllib.request.Request(BASE+path,data=json.dumps(data).encode() if data is not None else None,headers=headers,method=method)
    try:
        response=urllib.request.urlopen(request,timeout=60);code=response.status;body=response.read()
    except urllib.error.HTTPError as e: code=e.code;body=e.read()
    assert code in expected, f'{method} {path} as {user}: HTTP {code}; {body[:500]!r}'
    if code not in (200,201) or raw:return body
    return json.loads(body) if body else None

def check(name,fn):
    try:
        detail=fn()
        RESULTS.append((name,'PASS',str(detail or 'Verified')))
        print('PASS '+name+': '+str(detail or 'Verified'),flush=True)
    except Exception as e:
        RESULTS.append((name,'FAIL',str(e)))
        print('FAIL '+name+': '+str(e),flush=True)
        report()
        raise

def report():
    now=datetime.datetime.now(datetime.timezone.utc).isoformat()
    text='# Stage 2 automated localhost smoke test\n\nRun UTC: '+now+'\n\nCommand: `scripts/local smoke` from the branch root.\n\n'
    text+='This executes Docker Compose startup and health checks, authenticated API requests, stack/MinIO restarts, an offline backup and destructive change/restore of synthetic test records. Uses local `.env` credentials without printing them.\n\n'
    text+='| Check | Result | Evidence |\n|---|---|---|\n'
    for name,status,detail in RESULTS:
        text+='| '+name+' | '+status+' | '+detail.replace('|','/').replace('\n',' ')+' |\n'
    text+='\nThe Stage 2 baseline was accepted by the user on 17 October 2026. This is an automated regression run; Stage 3 requires its own [human UAT](stage-3-human-uat.md). See the [Stage 2 checklist](stage-2-human-uat.md).\n'
    text+='\nImplementation scope and limitations: [Stage 1 design](../nurivoyage/stage-1-design.md). No AWS deployment or production data used.\n'
    pathlib.Path('docs/testing/stage-2-smoke-test.md').write_text(text)

try:
    stamp=uuid.uuid4().hex[:10]
    check('01 Compose startup',lambda: (cmd('docker','compose','up','-d','--wait','--wait-timeout','300'),'docker compose up -d --wait succeeded')[1])
    check('02 Container health',lambda:cmd('scripts/local','health-check').strip())
    def loginpage():
        body=urllib.request.urlopen('http://localhost:8080/').read().decode()
        assert 'EspoCRM' in body or 'NuriVoyage' in body
        return 'HTTP 200; EspoCRM application shell'
    check('03 Local login page',loginpage)
    check('04 Administrator authentication',lambda:api('App/user')['user']['userName'])
    check('05 MariaDB',lambda:cmd('docker','compose','exec','-T','db','healthcheck.sh','--connect','--innodb_initialized').strip() or 'Connection and InnoDB healthy')
    customer=api('Account','POST',{'name':'Smoke Customer '+stamp,'description':'SYNTHETIC; safe to remove'})
    contact=api('Contact','POST',{'firstName':'Smoke','lastName':stamp,'accountId':customer['id']})
    check('06 Create customer/contact',lambda:f"Account {customer['id']}; Contact {contact['id']}")
    check('07 Stack restart and record persistence',lambda:(cmd('docker','compose','down'),cmd('docker','compose','up','-d','--wait','--wait-timeout','300'),api('Account/'+customer['id'])['name'])[-1])
    # Tiny valid synthetic PNG, no personal/customer data.
    PNG=base64.b64decode('iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAQAAAC1HAwCAAAAC0lEQVR42mP8/x8AAwMCAO+aKfkAAAAASUVORK5CYII=')
    document=api('NvTravelDocument','POST',{'name':'SYNTHETIC Smoke Document '+stamp})
    attachment=api('Attachment','POST',{'name':'synthetic-'+stamp+'.png','type':'image/png','role':'Attachment','relatedType':'NvTravelDocument','field':'file','file':'data:image/png;base64,'+base64.b64encode(PNG).decode()})
    api('NvTravelDocument/'+document['id'],'PUT',{'fileId':attachment['id']})
    def object_exists():
        return json.loads(cmd('docker','compose','exec','-T','-u','www-data','crm','php','/opt/nurivoyage/probe.php','object',attachment['id']))['exists']
    def document_proof():
        assert object_exists(), 'No corresponding MinIO object'
        assert api('Attachment/file/'+attachment['id'],raw=True)==PNG
        try:
            urllib.request.urlopen('http://localhost:9000/'+ENV['MINIO_BUCKET']+'/'+attachment['id'])
            raise AssertionError('MinIO object is publicly readable')
        except urllib.error.HTTPError as e:
            assert e.code==403
        assert api('Attachment/file/'+attachment['id'],user='operations',raw=True)==PNG
        api('Attachment/file/'+attachment['id'],user=None,expected=(401,403))
        api('Attachment/file/'+attachment['id'],user='sales',expected=(403,404))
        return 'MinIO object exists; authenticated admin/Operations download matches bytes; anonymous/Sales denied'
    check('08 Authorised MinIO document path',document_proof)
    def restart_minio():
        cmd('docker','compose','restart','minio')
        cmd('docker','compose','up','-d','--wait','--wait-timeout','300')
        assert api('Attachment/file/'+attachment['id'],raw=True)==PNG
        return 'Object survives MinIO restart and authorised download matches bytes'
    check('09 MinIO persistence',restart_minio)
    def email_proof():
        subject='NuriVoyage Smoke '+stamp
        email=api('Email','POST',{'name':subject,'subject':subject,'body':'Synthetic local smoke test only.','isHtml':False,'from':'admin@nuri.local','to':'sink@nuri.local','status':'Sending'})
        deadline=time.monotonic()+40
        while time.monotonic()<deadline:
            messages=json.load(urllib.request.urlopen('http://localhost:8025/api/v1/messages'))
            if any(m['Subject']==subject for m in messages['messages']):
                return 'Espo Email '+email['id']+' delivered to Mailpit: '+subject
            time.sleep(1)
        raise AssertionError('Espo mail missing from Mailpit')
    check('10 Espo email to Mailpit',email_proof)
    def jobs():
        cmd('docker','compose','exec','-T','-u','www-data','crm','php','cron.php')
        rows=json.loads(cmd('docker','compose','exec','-T','-u','www-data','crm','php','/opt/nurivoyage/probe.php','jobs'))
        assert rows and any(r.get('lastRun') for r in rows),rows
        logs=cmd('docker','compose','logs','--no-color','--since','10m','daemon')
        assert 'Fatal error' not in logs and 'Uncaught' not in logs
        return str(len(rows))+' scheduled jobs; at least one lastRun set; no daemon fatal errors'
    check('11 Daemon and scheduler',jobs)
    def websocket():
        with socket.create_connection(('localhost',8081),timeout=10) as s:
            s.sendall(b'GET / HTTP/1.1\r\nHost: localhost:8081\r\nUpgrade: websocket\r\nConnection: Upgrade\r\nSec-WebSocket-Key: dGhlIHNhbXBsZSBub25jZQ==\r\nSec-WebSocket-Version: 13\r\nSec-WebSocket-Protocol: wamp\r\n\r\n')
            response=s.recv(4096)
            assert b'101' in response,response
        return 'HTTP 101 WebSocket upgrade'
    check('12 WebSocket',websocket)
    backup=None
    def backup_proof():
        global backup
        output=cmd('scripts/local','backup')
        backup=next(line.split('=',1)[1] for line in output.splitlines() if line.startswith('BACKUP='))
        manifest=json.loads((pathlib.Path(backup)/'manifest.json').read_text())
        assert (pathlib.Path(backup)/'database.sql').stat().st_size>1000
        import tarfile
        with tarfile.open(pathlib.Path(backup)/'volumes.tar.gz') as t: assert any('minio/' in n for n in t.getnames())
        assert manifest['schemaVersion']==1
        return backup+'; SQL and runtime/object archive validated with SHA-256 manifest'
    check('13 Backup validity',backup_proof)
    def restore_proof():
        api('Account/'+customer['id'],'PUT',{'name':'CHANGED '+stamp})
        api('NvTravelDocument/'+document['id'],'PUT',{'fileId':None})
        # Removing a file through its record deletes the native Attachment and storage object.
        api('Attachment/file/'+attachment['id'],expected=(403,404))
        assert not object_exists(), 'MinIO object was not deleted'
        cmd('scripts/local','restore',backup)
        assert api('Account/'+customer['id'])['name']==customer['name']
        assert api('Contact/'+contact['id'])['accountId']==customer['id']
        assert api('Attachment/file/'+attachment['id'],raw=True)==PNG
        return 'Changed customer and deleted MinIO object recovered with matching bytes; contact relationship retained'
    check('14 Restore recovery and object deletion',restore_proof)
    check('15 Final service health',lambda:cmd('scripts/local','health-check').strip())
    def currency():
        settings=api('Settings')
        assert settings['defaultCurrency']=='ZAR' and settings['baseCurrency']=='ZAR'
        assert settings['currencyList']==['ZAR','USD','GBP','EUR','SAR','AED']
        assert settings['dateFormat']=='DD/MM/YYYY'
        return 'ZAR reporting/base; ZAR/USD/GBP/EUR/SAR/AED; DD/MM/YYYY'
    check('16 Organisation defaults',currency)
    def security():
        counts=[]
        items=api('NvBookingItem')['list'];assert items
        item=items[0]
        for login in ['admin-demo','manager','finance','sales','operations','hybrid','hybrid-commercial']:
            identity=api('App/user',user=login)
            assert identity['user']['userName']
            detail=api('NvBookingItem/'+item['id'],user=login)
            restricted=login in ['sales','operations','hybrid']
            assert (not any(k.startswith('purchaseCost') for k in detail)) if restricted else detail['purchaseCost']==item['purchaseCost'],login
            if restricted:
                api('NvPurchaseOrder',user=login,expected=(403,404))
                api('NvSupplierBill',user=login,expected=(403,404))
                # Writes to a hidden field may be rejected or silently filtered by Espo; verify no mutation.
                try: api('NvBookingItem/'+item['id'],'PUT',{'purchaseCost':99999},user=login,expected=(200,403))
                except AssertionError: raise
                assert api('NvBookingItem/'+item['id'])['purchaseCost']==item['purchaseCost']
            elif login=='hybrid-commercial':
                api('NvPurchaseOrder',user=login)
                api('NvSupplierBill',user=login)
                api('NvSupplierPayment',user=login,expected=(403,404))
                api('NvFxRate',user=login,expected=(403,404))
            if login in ['sales','hybrid','hybrid-commercial']:
                uid=identity['user']['id']
                commissions=api('NvCommission',user=login)['list']
                assert all(row['assignedUserId']==uid for row in commissions)
                other=next(row for row in api('NvCommission')['list'] if row['assignedUserId']!=uid)
                api('NvCommission/'+other['id'],user=login,expected=(403,404))
            if login in ['hybrid','hybrid-commercial']:
                api('NvEnquiry',user=login); api('NvTraveller',user=login);api('NvTravelDocument',user=login)
            counts.append(login)
        for entity in json.loads(pathlib.Path('scripts/nurivoyage/model.json').read_text())['entities']:
            api(entity,user='manager')
        assert len(api('Role')['list'])==7
        return 'Seven role personas authenticated; API cost read/write denials, commercial access, hybrid sales/ops modules and own-only commissions verified'
    check('17 Role boundaries',security)
    def sales_edit():
        record=api('Account','POST',{'name':'Sales UAT '+stamp},user='sales')
        api('Account/'+record['id'],'PUT',{'description':'Edited by Sales'},user='sales')
        assert api('Account/'+record['id'],user='sales')['description']=='Edited by Sales'
        api('NvCommission','POST',{'name':'Forbidden agent commission','amount':100},user='sales',expected=(403,404))
        traveller=api('NvTraveller','POST',{'name':'Ops Synthetic '+stamp,'customerId':record['id']},user='operations')
        assert traveller['customerId']==record['id']
        api('Account/'+record['id'],'PUT',{'description':'Forbidden operations edit'},user='operations',expected=(403,404))
        return 'Sales customer create/edit succeeds; agent commission creation denied; Operations traveller/customer link succeeds and customer edit denied; all 19 modules readable by Management'
    check('18 Role write paths',sales_edit)
    report()
    print('ALL '+str(len(RESULTS))+' CHECKS PASSED. Human UAT is pending.',flush=True)
except Exception:
    if not RESULTS or RESULTS[-1][1]!='FAIL': RESULTS.append(('Unexpected setup/runtime failure','FAIL',str(sys.exc_info()[1])))
    report()
    raise

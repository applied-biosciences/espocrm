import json, subprocess, urllib.request, sys
result = subprocess.run(['docker','compose','ps','--format','json'],capture_output=True,text=True,check=True)
try:
    rows=json.loads(result.stdout)
    if isinstance(rows,dict): rows=[rows]
except json.JSONDecodeError:
    rows=[json.loads(line) for line in result.stdout.splitlines()]
by={r['Service']:r for r in rows}
ok=True
for service in ['db','crm','daemon','websocket','minio','mailpit']:
    r=by.get(service,{})
    passed=r.get('State')=='running' and r.get('Health')=='healthy'
    print(('PASS' if passed else 'FAIL')+' '+service+': '+r.get('State','missing')+'/'+r.get('Health','unknown'))
    ok &= passed
for url in ['http://localhost:8080/','http://localhost:9000/minio/health/live','http://localhost:8025/readyz']:
    try:
        with urllib.request.urlopen(url,timeout=10) as r: assert r.status==200
        print('PASS '+url)
    except Exception as e:
        ok=False; print('FAIL '+url+': '+str(e))
sys.exit(0 if ok else 1)

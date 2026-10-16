"""Offline application snapshots. Never run concurrently with bootstrap or smoke tests."""
import subprocess, sys, pathlib, datetime, hashlib, json, os
DC=['docker','compose']
WRITERS=['crm','daemon','websocket','minio','mailpit']
def run(args,**kw): return subprocess.run(DC+args,check=True,**kw)
def digest(p):return hashlib.sha256(p.read_bytes()).hexdigest()
mode=sys.argv[1]
if mode=='backup':
    p=pathlib.Path('backups')/datetime.datetime.now(datetime.timezone.utc).strftime('%Y%m%dT%H%M%S%fZ')
    p.mkdir(parents=True,mode=0o700)
else:
    p=pathlib.Path(sys.argv[2]).resolve()
    manifest=json.loads((p/'manifest.json').read_text())
    assert manifest['schemaVersion']==1, 'Unsupported schema snapshot'
    for name,sha in manifest['sha256'].items():
        assert digest(p/name)==sha, 'Snapshot checksum mismatch: '+name
run(['stop']+WRITERS)
try:
    if mode=='backup':
        with (p/'database.sql').open('wb') as out:
            run(['exec','-T','db','sh','-ec','exec mariadb-dump -u"$MARIADB_USER" -p"$MARIADB_PASSWORD" --single-transaction --routines --triggers "$MARIADB_DATABASE"'],stdout=out)
        with (p/'volumes.tar.gz').open('wb') as out:
            run(['run','--rm','--no-deps','-T','maintenance','tar','czf','-','-C','/snapshot','espo','minio','mailpit'],stdout=out)
        (p/'manifest.json').write_text(json.dumps({'schemaVersion':1,'createdUtc':datetime.datetime.now(datetime.timezone.utc).isoformat(),
            'sha256':{name:digest(p/name) for name in ['database.sql','volumes.tar.gz']}},indent=2)+'\n')
        for f in p.iterdir(): f.chmod(0o600)
        print('BACKUP='+str(p),flush=True)
    else:
        with (p/'database.sql').open('rb') as data:
            run(['exec','-T','db','sh','-ec','exec mariadb -u"$MARIADB_USER" -p"$MARIADB_PASSWORD" "$MARIADB_DATABASE"'],stdin=data)
        with (p/'volumes.tar.gz').open('rb') as data:
            run(['run','--rm','--no-deps','-T','maintenance','sh','-ec',
                'find /snapshot/espo /snapshot/minio /snapshot/mailpit -mindepth 1 -maxdepth 1 -exec rm -rf {} +; tar xzf - -C /snapshot'],stdin=data)
        print('RESTORED='+str(p),flush=True)
finally:
    run(['up','-d','--wait','--wait-timeout','300'])

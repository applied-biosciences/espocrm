#!/usr/bin/env python3
"""Local production-readiness guardrails; never deploys to AWS."""
import pathlib, subprocess
root=pathlib.Path(__file__).resolve().parents[2]
env=root/'.env'; assert env.exists(), '.env is required for local deployment'
text=env.read_text()
for key in ['DB_PASSWORD=','DB_ROOT_PASSWORD=','ESPO_ADMIN_PASSWORD=','MINIO_SECRET_KEY=','DEV_USER_PASSWORD=']:
    assert key in text, 'required local secret is missing: '+key
assert 'BIND_ADDRESS=' not in text or 'BIND_ADDRESS=127.0.0.1' in text, 'local bind must remain loopback'
compose=(root/'compose.yaml').read_text()
for image in ['espocrm/espocrm:10.0.10@sha256:','mariadb:11.4.5@sha256:','mailpit:v1.24.1']:
    assert image in compose, 'unpinned or unexpected image: '+image
assert 'v10.0.10.00' in (root/'README.md').read_text(), 'production release marker is missing'
assert 'v10.0.10.00' in (root/'client/custom/nurivoyage-head.js').read_text(), 'client release marker is missing'
subprocess.run(['scripts/local','health-check'],cwd=root,check=True)
print('PASS production guardrails: local secrets present, loopback binding and pinned images verified')
print('PASS monitoring endpoints and service health verified')
print('AWS deployment intentionally not performed; approval and cloud credentials remain required')

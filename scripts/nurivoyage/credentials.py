"""Write a private local handoff sheet. Never commit this generated file."""
from pathlib import Path
import os
values=dict(line.split('=',1) for line in Path('.env').read_text().splitlines() if line and not line.startswith('#'))
p=Path('.local');p.mkdir(exist_ok=True,mode=0o700)
body='# Local NuriVoyage test credentials\n\nCRM: http://localhost:8080\nMailpit: http://localhost:8025\n\n'
body+='All seven synthetic role logins use this local test password:\n\n`'+values['DEV_USER_PASSWORD']+'`\n\n'
body+='| Role | Username |\n|---|---|\n'
for user,role in [('admin','System Administrator'),('manager','Management'),('finance','Finance'),('sales','Sales Agent'),('operations','Operations'),('hybrid','Sales + Operations Hybrid'),('hybrid-commercial','Sales + Operations Commercial')]:
    body+=f'| {role} | {user}@nuri.local |\n'
body+='\nBootstrap maintenance login: `'+values['ESPO_ADMIN_USERNAME']+'` / `'+values['ESPO_ADMIN_PASSWORD']+'`\n'
body+='\nReset role passwords: `scripts/local reset-passwords` (uses DEV_USER_PASSWORD from .env).\n'
body+='\nMinIO console: http://localhost:9001 ; user `'+values['MINIO_ACCESS_KEY']+'` ; password `'+values['MINIO_SECRET_KEY']+'`.\n'
body+='\nLocal development only. This sheet and .env are ignored by Git.\n'
out=p/'test-credentials.md';out.write_text(body);out.chmod(0o600)
print('Credentials written to .local/test-credentials.md (mode 0600).')

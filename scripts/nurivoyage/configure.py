"""Create local-only random credentials; never print them in logs."""
from pathlib import Path
import secrets, os
p = Path('.env')
if p.exists():
    if 'CHANGE_ME' in p.read_text():
        raise SystemExit('Replace CHANGE_ME placeholders in .env before starting.')
    print('.env exists; preserved.')
else:
    content = Path('.env.example').read_text()
    while 'CHANGE_ME' in content:
        content = content.replace('CHANGE_ME', secrets.token_hex(20), 1)
    fd = os.open(p, os.O_WRONLY | os.O_CREAT | os.O_EXCL, 0o600)
    with os.fdopen(fd, 'w') as out:
        out.write(content)
    print('Created .env with random local credentials (mode 0600).')

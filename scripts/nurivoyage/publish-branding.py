"""Copy original, user-supplied assets unchanged and publish static design previews."""
from pathlib import Path
import shutil
root=Path(__file__).resolve().parents[2]
source=root/'branding';target=root/'client/custom/branding'
target.mkdir(exist_ok=True,parents=True)
for src,name in [('logo/utnt-logo.png','utnt-logo.png'),('favicon/plane.png','plane.png')]:
    shutil.copyfile(source/src,target/name)
(target/'pdf').mkdir(exist_ok=True)
for p in (source/'pdf').glob('*.html'):
    (target/'pdf'/p.name).write_text(p.read_text().replace('../logo/utnt-logo.png','../utnt-logo.png').replace('../favicon/plane.png','../plane.png'))
for p in (source/'email').glob('*.html'):
    shutil.copyfile(p,root/'scripts/nurivoyage/branding-email'/p.name)
print('Published original logo/favicon and three static PDF-layout previews.')

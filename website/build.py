#!/usr/bin/env python3
from pathlib import Path
import shutil

ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / 'website'
DIST = SOURCE / 'dist'
IDENTITY = ROOT / 'assets' / 'identity' / 'official' / 'fold'

if DIST.exists():
    shutil.rmtree(DIST)
(DIST / 'assets').mkdir(parents=True)

for name in ('index.html', '404.html', '_headers'):
    shutil.copy2(SOURCE / name, DIST / name)

for name in ('site.css', 'identity.css', 'site.js'):
    shutil.copy2(SOURCE / name, DIST / 'assets' / name)

for name in (
    'glaze.css', 'glaze.controls.css', 'glaze.expressive.css', 'glaze.formfactors.css',
    'glaze.accessibility.css', 'glaze.color.css', 'glaze.motion.css', 'glaze.materials.css',
    'glaze.layout.css', 'glaze.states.css',
):
    shutil.copy2(ROOT / 'css' / name, DIST / 'assets' / name)

for name in ('glaze-ui-mark.svg', 'glaze-ui-lockup.svg'):
    shutil.copy2(IDENTITY / name, DIST / 'assets' / name)

print(f'Built {DIST.relative_to(ROOT)} from canonical Glaze UI source')

#!/usr/bin/env python3
from pathlib import Path
import shutil

ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / 'website'
DIST = SOURCE / 'dist'
IDENTITY = ROOT / 'assets/identity/official/facet'

if DIST.exists():
    shutil.rmtree(DIST)
(DIST / 'assets').mkdir(parents=True)

for name in ('index.html', '404.html', '_headers'):
    shutil.copy2(SOURCE / name, DIST / name)
for name in ('site.css', 'identity.css', 'site.js'):
    shutil.copy2(SOURCE / name, DIST / 'assets' / name)

# Production pages consume the Stable entrypoint. The immutable promoted
# Candidate snapshot is copied only because glaze-2.0.0.css imports it by its
# historical provenance filename; pages never link the Candidate directly.
for name in ('glaze-2.0.0.css', 'glaze-2.candidate.css'):
    shutil.copy2(ROOT / 'css' / name, DIST / 'assets' / name)

shutil.copy2(IDENTITY / 'glaze-ui-mark.svg', DIST / 'assets' / 'glaze-ui-mark.svg')
print(f'Built {DIST.relative_to(ROOT)} from the Glaze UI 2.0.0 Stable entrypoint and synchronized Facet identity')

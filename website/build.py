#!/usr/bin/env python3
from pathlib import Path
import shutil
ROOT=Path(__file__).resolve().parents[1]
SOURCE=ROOT/'website'; DIST=SOURCE/'dist'; IDENTITY=ROOT/'assets/identity/official/facet'
if DIST.exists(): shutil.rmtree(DIST)
(DIST/'assets').mkdir(parents=True)
for name in ('index.html','404.html','_headers'): shutil.copy2(SOURCE/name,DIST/name)
for name in ('site.css','identity.css','site.js'): shutil.copy2(SOURCE/name,DIST/'assets'/name)
for name in (
    'glaze.css','glaze.controls.css','glaze.expressive.css','glaze.formfactors.css','glaze.accessibility.css',
    'glaze.color.css','glaze.motion.css','glaze.materials.css','glaze.layout.css','glaze.states.css','glaze.workspace.candidate.css',
    'glaze-2.candidate.css','glaze-2.foldable.candidate.css','glaze-2.emerging.candidate.css',
): shutil.copy2(ROOT/'css'/name,DIST/'assets'/name)
shutil.copy2(IDENTITY/'glaze-ui-mark.svg',DIST/'assets'/'glaze-ui-mark.svg')
print(f'Built {DIST.relative_to(ROOT)} from Glaze UI 2.0 Stable source and synchronized Facet identity')

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
    # Retained 2.1 historical Stable regression/published rollback assets.
    'glaze-2.1.0.css','glaze-2.1.reference.css','glaze-2.1.visual-excellence.css',
    'glaze-2.1.visual-excellence.core.css','glaze-2.1.visual-excellence.review2.css',
    'glaze-2.1.visual-excellence.review3.css','glaze-2.1.visual-excellence.review4.css',
    # Current 2.2 Stable entrypoint and preserved promotion-source layers it imports.
    'glaze-2.2.0.css','glaze-2.2.candidate.css','glaze-2.2.components.candidate.css',
    'glaze-2.2.components.adaptive.candidate.css','glaze-2.2.components.runtime.candidate.css',
    'glaze-2.2.structure.candidate.css','glaze-2.2.overlay.candidate.css','glaze-2.2.advanced.candidate.css',
    'glaze-2.2.visual-refinement.candidate.css','glaze-2.2.optical-reachability.candidate.css',
): shutil.copy2(ROOT/'css'/name,DIST/'assets'/name)
shutil.copy2(IDENTITY/'glaze-ui-mark.svg',DIST/'assets'/'glaze-ui-mark.svg')
print(f'Built {DIST.relative_to(ROOT)} from Glaze UI 2.2.0 Stable source, retained 2.1 rollback assets, and synchronized Facet identity')

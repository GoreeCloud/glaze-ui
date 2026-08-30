#!/usr/bin/env python3
from pathlib import Path
import hashlib,re,subprocess,sys
ROOT=Path(__file__).resolve().parents[1]; SITE=ROOT/'website'; DIST=SITE/'dist'; IDENTITY=ROOT/'assets/identity/official/facet'
CANONICAL_SHA256='3c9566bf21c5bed4121547c3d5c79c34e4f3e60105179b7f2342c4b60ae91a61'
for n in ('index.html','404.html','site.css','identity.css','site.js','_headers','build.py'):
    if not (SITE/n).is_file(): raise SystemExit(f'missing website source: {n}')
for forbidden in (ROOT/'assets/identity/candidates/round-4',ROOT/'assets/identity/official/fold'):
    if forbidden.exists(): raise SystemExit(f'non-canonical identity path must not exist: {forbidden.relative_to(ROOT)}')
mark=IDENTITY/'glaze-ui-mark.svg'
if not mark.is_file() or hashlib.sha256(mark.read_bytes()).hexdigest()!=CANONICAL_SHA256: raise SystemExit('synchronized Facet source missing or changed')
subprocess.run([sys.executable,str(SITE/'build.py')],cwd=ROOT,check=True)
required=(
 'index.html','404.html','_headers','assets/glaze.css','assets/glaze.controls.css','assets/glaze.expressive.css','assets/glaze.formfactors.css','assets/glaze.accessibility.css','assets/glaze.color.css','assets/glaze.motion.css','assets/glaze.materials.css','assets/glaze.layout.css','assets/glaze.states.css','assets/glaze.workspace.candidate.css','assets/glaze-2.candidate.css','assets/glaze-2.foldable.candidate.css','assets/glaze-2.emerging.candidate.css','assets/glaze-2.1.0.css','assets/glaze-2.1.reference.css','assets/glaze-2.1.visual-excellence.css','assets/glaze-2.1.visual-excellence.core.css','assets/glaze-2.1.visual-excellence.review2.css','assets/glaze-2.1.visual-excellence.review3.css','assets/glaze-2.1.visual-excellence.review4.css','assets/site.css','assets/identity.css','assets/site.js','assets/glaze-ui-mark.svg')
for n in required:
    if not (DIST/n).is_file(): raise SystemExit(f'missing build artifact: {n}')
if (DIST/'assets/glaze-ui-mark.svg').read_bytes()!=mark.read_bytes(): raise SystemExit('public identity asset drifted from Facet source')
html=(DIST/'index.html').read_text(); headers=(DIST/'_headers').read_text(); js=(DIST/'assets/site.js').read_text(); core=(DIST/'assets/glaze-2.candidate.css').read_text(); emerging=(DIST/'assets/glaze-2.emerging.candidate.css').read_text(); foldable=(DIST/'assets/glaze-2.foldable.candidate.css').read_text(); stable=(DIST/'assets/glaze-2.1.0.css').read_text(); stable_ref=(DIST/'assets/glaze-2.1.reference.css').read_text(); glass=(DIST/'assets/glaze-2.1.visual-excellence.review4.css').read_text()
for text in ('Glaze UI 2.1 Stable','Make interaction feel tangible.','Content is solid. Interaction is glazed.','Canvas / Surface / Soft Glaze / Glaze / Deep Glaze / Live Glaze','Facet','GoreeCloud/goreecloud-glaze-ui','Navigation Capsule','Wearable','Spatial','2.1 is Stable and is the production design-system target.','Glaze UI 2.0.0 is the immediately preceding historical Stable baseline','no downstream application becomes 2.1-conformant by declaration','Skip to content'):
    if text not in html: raise SystemExit(f'required public-site content missing: {text}')
for asset in ('/assets/glaze-ui-mark.svg','/assets/glaze-2.1.0.css','/assets/glaze-2.candidate.css','/assets/glaze-2.foldable.candidate.css','/assets/glaze-2.emerging.candidate.css'):
    if asset not in html: raise SystemExit(f'required current/historical asset not published: {asset}')
for marker in ('@import url("./glaze-2.1.reference.css")','@import url("./glaze-2.1.visual-excellence.css")'):
    if marker not in stable: raise SystemExit(f'2.1 Stable entrypoint missing: {marker}')
for marker in ('--g21-touch-min:48px','data-glaze-material-level="soft-glaze"','data-glaze-material-level="live-glaze"','forced-colors:active'):
    if marker not in stable_ref: raise SystemExit(f'2.1 reference contract missing: {marker}')
for marker in ('increase the perceptual glass/translucency character','semantic color coding','[data-glaze-material-level="deep-glaze"]','[data-glaze-material-level="live-glaze"]','Reduced Transparency / Solid remains deliberately non-translucent','forced-colors: active'):
    if marker not in glass: raise SystemExit(f'approved 2.1 Visual Excellence contract missing: {marker}')
# Historical 2.0 form-factor implementation remains published for retained
# foldable/wearable/spatial examples until separately versioned 2.1 adapters land.
for marker in ('--glaze-touch-min: 48px','.glaze-material-soft','.glaze-material-deep','.glaze-material-live','.glaze-navigation-capsule','prefers-reduced-motion','prefers-reduced-transparency','forced-colors'):
    if marker not in core: raise SystemExit(f'retained 2.0 compatibility contract missing: {marker}')
for marker in ('.glaze-foldable-layout','.glaze-foldable-hinge'):
    if marker not in foldable: raise SystemExit(f'foldable contract missing: {marker}')
for marker in ('--glaze-wearable-target: 48px','--glaze-spatial-target: 56px','.glaze-wearable-rotary-nav','.glaze-spatial-stage'):
    if marker not in emerging: raise SystemExit(f'wearable/spatial contract missing: {marker}')
for remote in re.findall(r'(?:src|href)=["\'](https?://[^"\']+)',html):
    if 'github.com/GoreeCloud/goreecloud-glaze-ui' not in remote: raise SystemExit(f'unexpected remote browser resource/link: {remote}')
for directive in ('Content-Security-Policy:',"frame-ancestors 'none'",'Permissions-Policy:','X-Content-Type-Options: nosniff'):
    if directive not in headers: raise SystemExit(f'required security header missing: {directive}')
if 'localStorage' not in js or 'data-theme-choice' not in html: raise SystemExit('local appearance preference contract missing')
print('Glaze UI Design Center validation passed: 2.1.0 Stable with approved color-coded Glaze Material, retained cross-environment references, and synchronized Facet identity')

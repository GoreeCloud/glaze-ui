#!/usr/bin/env python3
from pathlib import Path
import hashlib,re,subprocess,sys

ROOT=Path(__file__).resolve().parents[1]
SITE=ROOT/'website'; DIST=SITE/'dist'; IDENTITY=ROOT/'assets/identity/official/facet'
CANONICAL_SHA256='3c9566bf21c5bed4121547c3d5c79c34e4f3e60105179b7f2342c4b60ae91a61'

for n in ('index.html','404.html','site.css','identity.css','site.js','_headers','build.py'):
    if not (SITE/n).is_file(): raise SystemExit(f'missing website source: {n}')
for forbidden in (ROOT/'assets/identity/candidates/round-4',ROOT/'assets/identity/official/fold'):
    if forbidden.exists(): raise SystemExit(f'non-canonical identity path must not exist: {forbidden.relative_to(ROOT)}')
mark=IDENTITY/'glaze-ui-mark.svg'
if not mark.is_file() or hashlib.sha256(mark.read_bytes()).hexdigest()!=CANONICAL_SHA256:
    raise SystemExit('synchronized Facet source missing or changed')

subprocess.run([sys.executable,str(SITE/'build.py')],cwd=ROOT,check=True)

required=(
    'index.html','404.html','_headers',
    'assets/glaze.css','assets/glaze.controls.css','assets/glaze.expressive.css','assets/glaze.formfactors.css','assets/glaze.accessibility.css',
    'assets/glaze.color.css','assets/glaze.motion.css','assets/glaze.materials.css','assets/glaze.layout.css','assets/glaze.states.css','assets/glaze.workspace.candidate.css',
    'assets/glaze-2.candidate.css','assets/glaze-2.foldable.candidate.css','assets/glaze-2.emerging.candidate.css',
    'assets/glaze-2.1.0.css','assets/glaze-2.1.reference.css','assets/glaze-2.1.visual-excellence.css',
    'assets/glaze-2.1.visual-excellence.core.css','assets/glaze-2.1.visual-excellence.review2.css','assets/glaze-2.1.visual-excellence.review3.css','assets/glaze-2.1.visual-excellence.review4.css',
    'assets/glaze-2.2.0.css','assets/glaze-2.2.candidate.css','assets/glaze-2.2.components.candidate.css',
    'assets/glaze-2.2.components.adaptive.candidate.css','assets/glaze-2.2.components.runtime.candidate.css',
    'assets/glaze-2.2.structure.candidate.css','assets/glaze-2.2.overlay.candidate.css','assets/glaze-2.2.advanced.candidate.css',
    'assets/glaze-2.2.visual-refinement.candidate.css','assets/glaze-2.2.optical-reachability.candidate.css',
    'assets/site.css','assets/identity.css','assets/site.js','assets/glaze-ui-mark.svg',
)
for n in required:
    if not (DIST/n).is_file(): raise SystemExit(f'missing build artifact: {n}')
if (DIST/'assets/glaze-ui-mark.svg').read_bytes()!=mark.read_bytes():
    raise SystemExit('public identity asset drifted from Facet source')

html=(DIST/'index.html').read_text(encoding='utf-8')
not_found=(DIST/'404.html').read_text(encoding='utf-8')
headers=(DIST/'_headers').read_text(encoding='utf-8')
js=(DIST/'assets/site.js').read_text(encoding='utf-8')
core20=(DIST/'assets/glaze-2.candidate.css').read_text(encoding='utf-8')
emerging20=(DIST/'assets/glaze-2.emerging.candidate.css').read_text(encoding='utf-8')
foldable20=(DIST/'assets/glaze-2.foldable.candidate.css').read_text(encoding='utf-8')
stable21=(DIST/'assets/glaze-2.1.0.css').read_text(encoding='utf-8')
stable_ref21=(DIST/'assets/glaze-2.1.reference.css').read_text(encoding='utf-8')
glass21=(DIST/'assets/glaze-2.1.visual-excellence.review4.css').read_text(encoding='utf-8')
stable22=(DIST/'assets/glaze-2.2.0.css').read_text(encoding='utf-8')
base22=(DIST/'assets/glaze-2.2.candidate.css').read_text(encoding='utf-8')
optical22=(DIST/'assets/glaze-2.2.optical-reachability.candidate.css').read_text(encoding='utf-8')

for text in (
    'Glaze UI 2.2 Stable',
    'Solid where you read. Glazed where you interact.',
    'Workspace → Application → System Overlay → System Panel → Critical System',
    'one dominant Glaze panel plus one to three small floating Glaze controls',
    '32 bounded contracts across five tiers.',
    'Universal Search',
    'Control Center',
    '2.2 is Stable and is the production design-system target.',
    'Glaze UI 2.1.0 is the immediately preceding historical Stable rollback baseline.',
    'no downstream application becomes 2.2-conformant by declaration',
    'Facet','GoreeCloud/goreecloud-glaze-ui','Skip to content',
):
    if text not in html: raise SystemExit(f'required public-site 2.2 content missing: {text}')

for asset in (
    '/assets/glaze-ui-mark.svg','/assets/glaze-2.2.0.css','/assets/glaze-2.candidate.css','/assets/glaze-2.foldable.candidate.css','/assets/glaze-2.emerging.candidate.css'
):
    if asset not in html: raise SystemExit(f'required current/historical asset not published: {asset}')
if '/assets/glaze-2.1.0.css' in html:
    raise SystemExit('public current page must not load 2.1.0 as an active Stable stylesheet')
for text in ('Glaze UI 2.2','404 · Glaze UI 2.2 Stable','/assets/glaze-2.2.0.css'):
    if text not in not_found: raise SystemExit(f'2.2 404 surface missing: {text}')

for marker in (
    '@import url("./glaze-2.2.candidate.css")',
    '@import url("./glaze-2.2.components.candidate.css")',
    '@import url("./glaze-2.2.components.adaptive.candidate.css")',
    '@import url("./glaze-2.2.components.runtime.candidate.css")',
    '@import url("./glaze-2.2.structure.candidate.css")',
    '@import url("./glaze-2.2.overlay.candidate.css")',
    '@import url("./glaze-2.2.advanced.candidate.css")',
    '@import url("./glaze-2.2.visual-refinement.candidate.css")',
    '@import url("./glaze-2.2.optical-reachability.candidate.css")',
):
    if marker not in stable22: raise SystemExit(f'2.2 Stable entrypoint missing promotion source: {marker}')

for marker in (
    '--glz22-target-shell: 48px','--glz22-target-assisted: 56px','.glz22-workspace','.glz22-application',
    '.glz22-system-overlay','.glz22-system-panel','.glz22-critical-system','[data-glz-appearance="deep-dark"]',
    'prefers-reduced-motion','prefers-reduced-transparency','prefers-contrast: more','forced-colors: active',
):
    if marker not in base22: raise SystemExit(f'2.2 Stable foundation source missing: {marker}')

# The approved Optical Reachability layer must remain published and preserve its
# bounded presentation identity. Dedicated exact-head rendered/pixel workflows
# prove visual equivalence; this public-site validator protects source presence.
for marker in ('.glz22-', 'optical'):
    if marker.lower() not in optical22.lower(): raise SystemExit(f'2.2 Optical Reachability source missing marker: {marker}')

# Retain the full 2.1 Stable rollback/public regression contract.
for marker in ('@import url("./glaze-2.1.reference.css")','@import url("./glaze-2.1.visual-excellence.css")'):
    if marker not in stable21: raise SystemExit(f'retained 2.1 Stable entrypoint missing: {marker}')
for marker in ('--g21-touch-min:48px','data-glaze-material-level="soft-glaze"','data-glaze-material-level="live-glaze"','forced-colors:active'):
    if marker not in stable_ref21: raise SystemExit(f'retained 2.1 reference contract missing: {marker}')
for marker in ('increase the perceptual glass/translucency character','semantic color coding','[data-glaze-material-level="deep-glaze"]','[data-glaze-material-level="live-glaze"]','Reduced Transparency / Solid remains deliberately non-translucent','forced-colors: active'):
    if marker not in glass21: raise SystemExit(f'approved 2.1 Visual Excellence regression missing: {marker}')

# Historical 2.0 cross-environment implementation remains published for
# foldable/wearable/spatial compatibility and permanent regression evidence.
for marker in ('--glaze-touch-min: 48px','.glaze-material-soft','.glaze-material-deep','.glaze-material-live','.glaze-navigation-capsule','prefers-reduced-motion','prefers-reduced-transparency','forced-colors'):
    if marker not in core20: raise SystemExit(f'retained 2.0 compatibility contract missing: {marker}')
for marker in ('.glaze-foldable-layout','.glaze-foldable-hinge'):
    if marker not in foldable20: raise SystemExit(f'foldable contract missing: {marker}')
for marker in ('--glaze-wearable-target: 48px','--glaze-spatial-target: 56px','.glaze-wearable-rotary-nav','.glaze-spatial-stage'):
    if marker not in emerging20: raise SystemExit(f'wearable/spatial contract missing: {marker}')

for remote in re.findall(r'(?:src|href)=["\'](https?://[^"\']+)',html):
    if 'github.com/GoreeCloud/goreecloud-glaze-ui' not in remote:
        raise SystemExit(f'unexpected remote browser resource/link: {remote}')
for directive in ('Content-Security-Policy:',"frame-ancestors 'none'",'Permissions-Policy:','X-Content-Type-Options: nosniff'):
    if directive not in headers: raise SystemExit(f'required security header missing: {directive}')
if 'localStorage' not in js or 'data-theme-choice' not in html:
    raise SystemExit('local appearance preference contract missing')

print('Glaze UI Design Center validation passed: 2.2.0 Stable with System Shell/component/Optical Reachability guidance, retained 2.1 rollback and 2.0 cross-environment regressions, and synchronized Facet identity')

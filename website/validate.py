#!/usr/bin/env python3
from pathlib import Path
import hashlib
import re
import subprocess
import sys

ROOT = Path(__file__).resolve().parents[1]
SITE = ROOT / 'website'
DIST = SITE / 'dist'
IDENTITY = ROOT / 'assets' / 'identity' / 'official' / 'facet'
CANONICAL_SHA256 = '3c9566bf21c5bed4121547c3d5c79c34e4f3e60105179b7f2342c4b60ae91a61'

for n in ('index.html', '404.html', 'site.css', 'identity.css', 'site.js', '_headers', 'build.py'):
    if not (SITE / n).is_file():
        raise SystemExit(f'missing website source: {n}')

for forbidden in (
    ROOT / 'assets' / 'identity' / 'candidates' / 'round-4',
    ROOT / 'assets' / 'identity' / 'official' / 'fold',
):
    if forbidden.exists():
        raise SystemExit(f'non-canonical identity path must not exist: {forbidden.relative_to(ROOT)}')

mark = IDENTITY / 'glaze-ui-mark.svg'
if not mark.is_file():
    raise SystemExit('missing synchronized Glaze UI Facet source')
if hashlib.sha256(mark.read_bytes()).hexdigest() != CANONICAL_SHA256:
    raise SystemExit('synchronized Glaze UI Facet source does not match the approved SHA-256')

subprocess.run([sys.executable, str(SITE / 'build.py')], cwd=ROOT, check=True)

required = (
    'index.html', '404.html', '_headers',
    'assets/glaze.css', 'assets/glaze.controls.css', 'assets/glaze.expressive.css',
    'assets/glaze.formfactors.css', 'assets/glaze.accessibility.css',
    'assets/glaze.color.css', 'assets/glaze.motion.css', 'assets/glaze.materials.css',
    'assets/glaze.layout.css', 'assets/glaze.states.css', 'assets/glaze.workspace.candidate.css',
    'assets/site.css', 'assets/identity.css', 'assets/site.js',
    'assets/glaze-ui-mark.svg',
)
for n in required:
    if not (DIST / n).is_file():
        raise SystemExit(f'missing build artifact: {n}')

if (DIST / 'assets' / 'glaze-ui-mark.svg').read_bytes() != mark.read_bytes():
    raise SystemExit('public identity asset drifted from synchronized Facet source')

html = (DIST / 'index.html').read_text()
headers = (DIST / '_headers').read_text()
js = (DIST / 'assets' / 'site.js').read_text()
expressive = (DIST / 'assets' / 'glaze.expressive.css').read_text()
formfactors = (DIST / 'assets' / 'glaze.formfactors.css').read_text()
motion = (DIST / 'assets' / 'glaze.motion.css').read_text()
materials = (DIST / 'assets' / 'glaze.materials.css').read_text()
layout = (DIST / 'assets' / 'glaze.layout.css').read_text()
states = (DIST / 'assets' / 'glaze.states.css').read_text()
workspace = (DIST / 'assets' / 'glaze.workspace.candidate.css').read_text()

for n in (
    'Glaze UI 1.5 Stable',
    'One design language. Four interaction environments.',
    'Facet is the official Glaze UI mark.',
    'Official Glaze UI Facet mark',
    'Official Glaze UI Facet standalone mark',
    'GoreeCloud/goreecloud-branding-assets',
    'Mobile', 'Tablet', 'Desktop', 'TV',
    'Canvas', 'Solid', 'Raised', 'Functional Glass', 'Overlay',
    'Glaze UI 1.6 Candidate',
    'Adaptive workspace turns shell behavior into a shared contract.',
    'Candidate · production baseline remains 1.5.0',
    'Shared semantics, flexible composition',
    'Stable semantics protect beauty and usability',
    '1.5 is Stable and is the production target.',
    'Smartwatch and wearable applications remain production-blocked',
    'Skip to content',
):
    if n not in html:
        raise SystemExit(f'required public-site content missing: {n}')

for forbidden_text in ('Fold is the official Glaze UI mark.', 'Official Glaze UI Fold', 'glaze-ui-lockup.svg', 'authoritative SVG source lives in the Glaze UI repository'):
    if forbidden_text in html:
        raise SystemExit(f'legacy identity content must not be published: {forbidden_text}')

for asset in ('/assets/glaze-ui-mark.svg', '/assets/identity.css'):
    if asset not in html:
        raise SystemExit(f'required official identity asset not published: {asset}')

for s in (
    '/assets/glaze.controls.css', '/assets/glaze.expressive.css', '/assets/glaze.formfactors.css',
    '/assets/glaze.accessibility.css', '/assets/glaze.color.css', '/assets/glaze.motion.css',
    '/assets/glaze.materials.css', '/assets/glaze.layout.css', '/assets/glaze.states.css',
    '/assets/glaze.workspace.candidate.css',
):
    if s not in html:
        raise SystemExit(f'required stylesheet not loaded: {s}')

for m in ('.glaze-glass-functional', '.glaze-glass-clear', '.glaze-expressive-action', '.glaze-button-group', '.glaze-reach-layout', 'prefers-reduced-motion', 'prefers-reduced-transparency', 'forced-colors'):
    if m not in expressive:
        raise SystemExit(f'expressive contract missing: {m}')
for m in ('.glaze-mobile-shell', '.glaze-tablet-shell', '.glaze-desktop-shell', '.glaze-tv-shell', '.glaze-tv-focusable'):
    if m not in formfactors:
        raise SystemExit(f'form-factor contract missing: {m}')
for source, markers in (
    (motion, ('prefers-reduced-motion', 'glaze-motion-state')),
    (materials, ('glaze-material-functional-glass', 'glaze-material-solid')),
    (layout, ('glaze-container', 'glaze-scroll-x')),
    (states, ('focus-visible', 'aria-selected')),
    (workspace, ('.glaze-workspace-candidate', '.glaze-workspace-nav-candidate', '.glaze-workspace-toolbar-candidate', '.glaze-workspace-content-candidate', 'pointer: fine', 'pointer: coarse', 'forced-colors')),
):
    for marker in markers:
        if marker not in source:
            raise SystemExit(f'public contract missing: {marker}')

for remote in re.findall(r'(?:src|href)=["\'](https?://[^"\']+)', html):
    if 'github.com/GoreeCloud/goreecloud-glaze-ui' not in remote:
        raise SystemExit(f'unexpected remote browser resource/link: {remote}')

for d in ('Content-Security-Policy:', "frame-ancestors 'none'", 'Permissions-Policy:', 'X-Content-Type-Options: nosniff'):
    if d not in headers:
        raise SystemExit(f'required security header missing: {d}')

if 'localStorage' not in js or 'data-theme-choice' not in html:
    raise SystemExit('local appearance preference contract missing')

print('Glaze UI Design Center validation passed: 1.5 Stable with bounded 1.6 Candidate preview and synchronized Facet identity')

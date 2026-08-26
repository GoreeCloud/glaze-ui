#!/usr/bin/env python3
from pathlib import Path
import re
import subprocess
import sys

ROOT = Path(__file__).resolve().parents[1]
SITE = ROOT / 'website'
DIST = SITE / 'dist'
IDENTITY = ROOT / 'assets' / 'identity' / 'official' / 'fold'

for n in ('index.html', '404.html', 'site.css', 'identity.css', 'site.js', '_headers', 'build.py'):
    if not (SITE / n).is_file():
        raise SystemExit(f'missing website source: {n}')

subprocess.run([sys.executable, str(SITE / 'build.py')], cwd=ROOT, check=True)

required = (
    'index.html', '404.html', '_headers',
    'assets/glaze.css', 'assets/glaze.controls.css', 'assets/glaze.expressive.css',
    'assets/glaze.formfactors.css', 'assets/glaze.accessibility.css',
    'assets/glaze.color.css', 'assets/glaze.motion.css', 'assets/glaze.materials.css',
    'assets/glaze.layout.css', 'assets/glaze.states.css',
    'assets/site.css', 'assets/identity.css', 'assets/site.js',
    'assets/glaze-ui-mark.svg', 'assets/glaze-ui-lockup.svg',
)
for n in required:
    if not (DIST / n).is_file():
        raise SystemExit(f'missing build artifact: {n}')

for name in ('glaze-ui-mark.svg', 'glaze-ui-lockup.svg'):
    if (DIST / 'assets' / name).read_bytes() != (IDENTITY / name).read_bytes():
        raise SystemExit(f'public identity asset drifted from canonical Fold source: {name}')

html = (DIST / 'index.html').read_text()
headers = (DIST / '_headers').read_text()
js = (DIST / 'assets' / 'site.js').read_text()
expressive = (DIST / 'assets' / 'glaze.expressive.css').read_text()
formfactors = (DIST / 'assets' / 'glaze.formfactors.css').read_text()
motion = (DIST / 'assets' / 'glaze.motion.css').read_text()
materials = (DIST / 'assets' / 'glaze.materials.css').read_text()
layout = (DIST / 'assets' / 'glaze.layout.css').read_text()
states = (DIST / 'assets' / 'glaze.states.css').read_text()

for n in (
    'Glaze UI 1.5 Stable',
    'One design language. Four interaction environments.',
    'Fold is the official Glaze UI mark.',
    'Official Glaze UI Fold mark',
    'Standalone mark',
    'Horizontal lockup',
    'Mobile', 'Tablet', 'Desktop', 'TV',
    'Canvas', 'Solid', 'Raised', 'Functional Glass', 'Overlay',
    'Shared semantics, flexible composition',
    'Stable semantics protect beauty and usability',
    '1.5 is Stable and is the production target.',
    'Smartwatch and wearable applications remain production-blocked',
    'Skip to content',
):
    if n not in html:
        raise SystemExit(f'required public-site content missing: {n}')

for asset in ('/assets/glaze-ui-mark.svg', '/assets/glaze-ui-lockup.svg', '/assets/identity.css'):
    if asset not in html:
        raise SystemExit(f'required official identity asset not published: {asset}')

for s in (
    '/assets/glaze.controls.css', '/assets/glaze.expressive.css', '/assets/glaze.formfactors.css',
    '/assets/glaze.accessibility.css', '/assets/glaze.color.css', '/assets/glaze.motion.css',
    '/assets/glaze.materials.css', '/assets/glaze.layout.css', '/assets/glaze.states.css',
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
):
    for marker in markers:
        if marker not in source:
            raise SystemExit(f'promoted 1.5 public contract missing: {marker}')

for remote in re.findall(r'(?:src|href)=["\'](https?://[^"\']+)', html):
    if 'github.com/GoreeCloud/glaze-ui' not in remote:
        raise SystemExit(f'unexpected remote browser resource/link: {remote}')

for d in ('Content-Security-Policy:', "frame-ancestors 'none'", 'Permissions-Policy:', 'X-Content-Type-Options: nosniff'):
    if d not in headers:
        raise SystemExit(f'required security header missing: {d}')

if 'localStorage' not in js or 'data-theme-choice' not in html:
    raise SystemExit('local appearance preference contract missing')

print('Glaze UI 1.5 Stable public design site validation passed')

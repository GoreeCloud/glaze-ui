#!/usr/bin/env python3
from pathlib import Path
import hashlib
import re
import subprocess
import sys

ROOT = Path(__file__).resolve().parents[1]
SITE = ROOT / 'website'
DIST = SITE / 'dist'
IDENTITY = ROOT / 'assets/identity/official/facet'
CANONICAL_SHA256 = '3c9566bf21c5bed4121547c3d5c79c34e4f3e60105179b7f2342c4b60ae91a61'

for name in ('index.html', '404.html', 'site.css', 'identity.css', 'site.js', '_headers', 'build.py'):
    if not (SITE / name).is_file():
        raise SystemExit(f'missing website source: {name}')
for forbidden in (ROOT / 'assets/identity/candidates/round-4', ROOT / 'assets/identity/official/fold'):
    if forbidden.exists():
        raise SystemExit(f'non-canonical identity path must not exist: {forbidden.relative_to(ROOT)}')

mark = IDENTITY / 'glaze-ui-mark.svg'
if not mark.is_file() or hashlib.sha256(mark.read_bytes()).hexdigest() != CANONICAL_SHA256:
    raise SystemExit('synchronized Facet source missing or changed')

subprocess.run([sys.executable, str(SITE / 'build.py')], cwd=ROOT, check=True)
required = (
    'index.html', '404.html', '_headers', 'assets/glaze-2.0.0.css',
    'assets/glaze-2.candidate.css', 'assets/site.css', 'assets/identity.css',
    'assets/site.js', 'assets/glaze-ui-mark.svg',
)
for name in required:
    if not (DIST / name).is_file():
        raise SystemExit(f'missing build artifact: {name}')
if (DIST / 'assets/glaze-ui-mark.svg').read_bytes() != mark.read_bytes():
    raise SystemExit('public identity asset drifted from Facet source')

html = (DIST / 'index.html').read_text(encoding='utf-8')
error_html = (DIST / '404.html').read_text(encoding='utf-8')
headers = (DIST / '_headers').read_text(encoding='utf-8')
js = (DIST / 'assets/site.js').read_text(encoding='utf-8')
stable = (DIST / 'assets/glaze-2.0.0.css').read_text(encoding='utf-8')
core = (DIST / 'assets/glaze-2.candidate.css').read_text(encoding='utf-8')

for text in (
    'Glaze UI 2.0.0 Stable', 'Make interaction feel tangible.',
    'Canvas / Surface / Soft Glaze / Glaze / Deep Glaze / Live Glaze',
    'Facet', 'GoreeCloud/goreecloud-glaze-ui', 'Navigation Capsule',
    'Wearable', 'Spatial', '2.0.0 is Stable and is the production target.',
    'Glaze UI 1.6.0 is the immediately preceding historical Stable baseline',
    'Glaze UI 2.1 remains Candidate',
    'no downstream application becomes 2.0-conformant by declaration', 'Skip to content',
):
    if text not in html:
        raise SystemExit(f'required public-site content missing: {text}')

for page_name, page in (('index', html), ('404', error_html)):
    if '/assets/glaze-2.0.0.css' not in page or 'data-glaze-ui="2.0.0"' not in page:
        raise SystemExit(f'{page_name} must consume the Glaze UI 2.0.0 Stable entrypoint')
    for direct_candidate in (
        '/assets/glaze-2.candidate.css', '/assets/glaze.workspace.candidate.css',
        '/assets/glaze-2.foldable.candidate.css', '/assets/glaze-2.emerging.candidate.css',
    ):
        if direct_candidate in page:
            raise SystemExit(f'{page_name} directly exposes Candidate dependency: {direct_candidate}')

if '@import url("./glaze-2.candidate.css")' not in stable:
    raise SystemExit('Stable 2.0.0 entrypoint no longer pins the promoted immutable implementation snapshot')
for marker in (
    '--glaze-touch-min: 48px', '.glaze-material-soft', '.glaze-material-deep',
    '.glaze-material-live', '.glaze-navigation-capsule', 'prefers-reduced-motion',
    'prefers-reduced-transparency', 'forced-colors',
):
    if marker not in core:
        raise SystemExit(f'2.0 core contract missing: {marker}')

for remote in re.findall(r'(?:src|href)=["\'](https?://[^"\']+)', html):
    if 'github.com/GoreeCloud/goreecloud-glaze-ui' not in remote:
        raise SystemExit(f'unexpected remote browser resource/link: {remote}')
for directive in ('Content-Security-Policy:', "frame-ancestors 'none'", 'Permissions-Policy:', 'X-Content-Type-Options: nosniff'):
    if directive not in headers:
        raise SystemExit(f'required security header missing: {directive}')
if 'localStorage' not in js or 'data-theme-choice' not in html:
    raise SystemExit('local appearance preference contract missing')

print('Glaze UI Design Center validation passed: 2.0.0 Stable entrypoint, no direct Candidate production dependency, synchronized Facet identity')

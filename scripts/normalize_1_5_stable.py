#!/usr/bin/env python3
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DOCS = [
    'COLOR_ARCHITECTURE.md', 'ICONOGRAPHY.md', 'ICON_CONSTRUCTION.md', 'ICON_IDENTITY.md',
    'MOTION.md', 'MATERIALS.md', 'LAYOUT.md', 'STATES.md',
]

for rel in DOCS:
    path = ROOT / rel
    if not path.is_file():
        raise SystemExit(f'missing active 1.5 contract: {rel}')
    text = path.read_text(encoding='utf-8')
    text = text.replace('Glaze UI 1.4.0 remains the mandatory Stable production target until 1.5 is promoted.', 'Glaze UI 1.5.0 is the current Stable production target.')
    text = text.replace('current Stable production target until 1.5 is promoted', 'current Stable 1.5.0 production target')
    text = text.replace('Glaze UI 1.5 Candidate', 'Glaze UI 1.5 Stable')
    text = text.replace('1.5 Candidate', '1.5 Stable')
    text = text.replace('Candidate', 'Stable')
    text = text.replace('candidate', 'stable')
    path.write_text(text, encoding='utf-8')

print('Normalized active Glaze UI 1.5 contracts to Stable lifecycle wording')

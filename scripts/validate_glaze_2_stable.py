#!/usr/bin/env python3
"""Validate Glaze UI 2.1.0 Stable and preserved 2.0/2.1 Candidate provenance."""
from pathlib import Path
import json
ROOT=Path(__file__).resolve().parents[1]
def req(c,m):
    if not c: raise SystemExit(f'Glaze UI 2.1 Stable validation failed: {m}')
def txt(p): return (ROOT/p).read_text(encoding='utf-8')
def main():
    req(txt('VERSION').strip()=='2.1.0','VERSION')
    for p in ('GLAZE_UI_2_1_STABLE.md','GLAZE_UI_2_STABLE.md','GLAZE_UI_2_1_CANDIDATE.md','acceptance/2.1-candidate.md','acceptance/2.1-stable.md','css/glaze-2.1.0.css','js/glaze-2.1.0.mjs','css/glaze-2.1.reference.css','css/glaze-2.1.visual-excellence.css','js/glaze-2.1.candidate.mjs'):
        req((ROOT/p).is_file(),f'missing {p}')
    req('@import url("./glaze-2.1.reference.css");' in txt('css/glaze-2.1.0.css'),'Stable CSS must bind 2.1 reference source')
    req('@import url("./glaze-2.1.visual-excellence.css");' in txt('css/glaze-2.1.0.css'),'Stable CSS must bind approved Visual Excellence layer')
    req('export * from "./glaze-2.1.candidate.mjs";' in txt('js/glaze-2.1.0.mjs'),'Stable runtime must bind preserved Candidate implementation')
    doc=txt('GLAZE_UI_2_1_STABLE.md')
    for m in ('Stable semantic version:** 2.1.0','Previous Stable implementation baseline:** Glaze UI 2.0.0','Approve Visual Excellence','Glaze Motion remains separately governed and Experimental'):
        req(m in doc,f'missing {m}')
    candidate=txt('acceptance/2.1-candidate.md')
    req('Approve Visual Excellence' in candidate and 'a21601691dc412baa6a889533d6fa5b3a7996dc2' in candidate,'approved Candidate provenance missing')
    lifecycle=json.loads(txt('registry/lifecycle.json'))
    req(lifecycle.get('currentStable')=='2.1.0' and lifecycle.get('activeCandidate') is None,'lifecycle not promoted')
    print('Glaze UI 2.1.0 Stable contract and preserved promotion provenance validated')
if __name__=='__main__': main()

#!/usr/bin/env python3
"""Focused fail-closed validation for the Glaze UI 2.1.0 Stable promotion."""
from pathlib import Path
import json
ROOT=Path(__file__).resolve().parents[1]
def req(c,m):
    if not c: raise SystemExit(f'Glaze UI 2.1 Stable promotion validation failed: {m}')
def text(p):
    q=ROOT/p; req(q.is_file(),f'missing {p}'); return q.read_text(encoding='utf-8')
def main():
    req(text('VERSION').strip()=='2.1.0','VERSION must be 2.1.0')
    lifecycle=json.loads(text('registry/lifecycle.json')); req(lifecycle['currentStable']=='2.1.0' and lifecycle['activeCandidate'] is None,'lifecycle')
    for cap in ('visual-excellence-gate','material-budgets','accessibility-resolution-matrix','canonical-reference-flows-2.1','visual-regression-2.1','android-native-reference-2.1'):
        req(lifecycle.get('capabilities',{}).get(cap,{}).get('status')=='stable',f'{cap} not Stable')
    manifest=json.loads(text('contracts/regression/visual-baselines.json')); req(manifest.get('baselineRevision')=='5b46903c18660ae78e7f1aaea39a93136efacda7','approved visual baseline revision')
    thresholds=manifest.get('thresholds',{}); req(thresholds.get('perChannelTolerance')==12 and thresholds.get('maxChangedPixelRatio')==0.0075 and thresholds.get('maxMeanAbsoluteChannelDelta')==1.5,'visual thresholds changed')
    accept=text('acceptance/2.1-stable.md'); req('Approve Visual Excellence' in accept,'human Visual Excellence acceptance')
    stable=text('GLAZE_UI_2_1_STABLE.md'); req('Content is solid. Interaction is glazed.' in stable,'core material rule')
    req('Reduced Transparency' in stable and 'Forced Colors' in stable,'accessibility precedence')
    req('No downstream application is promoted by declaration' in stable,'consumer boundary')
    print('Glaze UI 2.1.0 focused Stable promotion validation passed')
if __name__=='__main__': main()

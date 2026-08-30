#!/usr/bin/env python3
"""Fail-closed validation for the Glaze UI Stable form-factor contract retained from 1.5."""
from __future__ import annotations
import json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
def req(c,m):
    if not c: raise SystemExit(f'Glaze UI form-factor validation failed: {m}')
def text(p): return (ROOT/p).read_text(encoding='utf-8')
def main():
    for p in ('FORM_FACTORS.md','css/glaze.formfactors.css','reference/formfactors.html','reference/acceptance.html','acceptance/1.4.0.md','acceptance/1.5.0.md'):
        req((ROOT/p).is_file(),f'missing {p}')
    version=text('VERSION').strip()
    try: version_tuple=tuple(int(part) for part in version.split('.'))
    except ValueError: raise SystemExit('Glaze UI form-factor validation failed: VERSION must use semantic versioning')
    req(len(version_tuple)==3 and version_tuple>=(1,5,0),'current Stable VERSION must retain the 1.5-or-later form-factor contract')
    stable_family='.'.join(version.split('.')[:2])
    data=json.loads(text('tokens/glaze.tokens.json')); req(data['meta']['version']==version and data['meta']['status']=='Stable','token metadata must declare the current Stable VERSION'); req(data['meta']['stableBaseline']==version,'token Stable baseline must match VERSION')
    req(set(data['formFactor'])=={'mobile','tablet','desktop','tv'},'formFactor set must be Mobile/Tablet/Desktop/TV'); req(data['target']['tvMinimum']>=56,'TV target must be at least 56'); req(data['layout']['tvSafeMarginPercent']>=5,'TV safe margin must be at least 5%'); req(data['formFactor']['tv']['viewingDistance']=='far','TV viewing distance must be far'); req('directional' in data['formFactor']['tv']['primaryInput'],'TV primary input must be directional')
    css=text('css/glaze.formfactors.css')
    for m in ('.glaze-mobile-shell','.glaze-tablet-shell','.glaze-desktop-shell','.glaze-tv-shell','.glaze-tv-focusable','--glaze-tv-safe-inline','--glaze-tv-safe-block','prefers-reduced-motion','forced-colors'): req(m in css,f'form-factor CSS missing {m}')
    contract=text('FORM_FACTORS.md')
    for m in ('Mobile UI','Tablet UI','Desktop UI','TV UI','TV is defined primarily by far viewing distance','TV must never be treated as Wide Desktop','Glaze UI 1.4 Stable form-factor acceptance requires representative acceptance for every supported profile'):
        req(m in contract,f'FORM_FACTORS.md missing retained Stable contract marker {m}')
    req('A Glaze UI 1.4 candidate must include representative acceptance' not in contract,'FORM_FACTORS.md contains stale 1.4 Candidate acceptance wording')
    ref=text('reference/formfactors.html')
    for m in ('data-profile="mobile"','data-profile="tablet"','data-profile="desktop"','data-profile="tv"','ArrowLeft','ArrowRight','ArrowUp','ArrowDown'): req(m in ref,f'form-factor reference missing {m}')
    acceptance=text('ACCEPTANCE.md')
    for m in ('390 × 844','820 × 1180','1280 × 900','1600 × 1000','1920 × 1080','directional focus','overscan-safe','dependency-free Mobile/Tablet/Desktop/Wide Desktop/TV references'):
        req(m in acceptance,f'acceptance missing {m}')
    req('dependency-free Mobile/Tablet/Desktop/TV references' not in acceptance,'acceptance contains incomplete four-profile reference wording')
    readme=text('README.md')
    req(f'Glaze UI {version} is the current Stable canonical baseline' in readme,'README current Stable statement missing')
    req('dependency-free five-profile reference' in readme,'README must retain the five-profile Stable form-factor reference')
    req('dependency-free four-profile reference' not in readme,'README contains stale four-profile form-factor wording')
    for m in ('Mobile 390×844','Tablet 820×1180','Desktop 1280×900','Wide Desktop 1600×1000','TV 1920×1080'):
        req(m in readme,f'README Stable form-factor matrix missing {m}')
    lifecycle=text('COMPONENT_STATUS.md')
    req('Glaze UI 1.4 Stable form-factor layer' in lifecycle,'retained 1.4 form-factor lifecycle record missing')
    req('Glaze UI 1.5 Stable systems' in lifecycle,'retained 1.5 Stable lifecycle promotion missing')
    req(f'Stable baseline:** Glaze UI **{version}' in text('STABILITY.md'),'current stability baseline missing')
    req(json.loads(text('consumers/registry.json'))['stableBaseline']==version,'current consumer baseline missing')
    req(f'Glaze UI {stable_family} Stable' in text('website/index.html'),'public site current Stable marker missing')
    print(f'Glaze UI {version} retained Stable form-factor source validation passed')
if __name__=='__main__': main()

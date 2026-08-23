#!/usr/bin/env python3
"""Fail-closed Glaze UI 1.4 Stable form-factor validation."""
from __future__ import annotations
import json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
def req(c,m):
    if not c: raise SystemExit(f'Glaze UI form-factor validation failed: {m}')
def text(p): return (ROOT/p).read_text(encoding='utf-8')
def main():
    for p in ('FORM_FACTORS.md','css/glaze.formfactors.css','reference/formfactors.html','reference/acceptance.html','acceptance/1.4.0.md'):
        req((ROOT/p).is_file(),f'missing {p}')
    req(text('VERSION').strip()=='1.4.0','VERSION must be 1.4.0')
    data=json.loads(text('tokens/glaze.tokens.json')); req(data['meta']['version']=='1.4.0' and data['meta']['status']=='Stable','token metadata must declare 1.4.0 Stable'); req(data['meta']['stableBaseline']=='1.4.0','token Stable baseline must be 1.4.0')
    req(set(data['formFactor'])=={'mobile','tablet','desktop','tv'},'formFactor set must be Mobile/Tablet/Desktop/TV'); req(data['target']['tvMinimum']>=56,'TV target must be at least 56'); req(data['layout']['tvSafeMarginPercent']>=5,'TV safe margin must be at least 5%'); req(data['formFactor']['tv']['viewingDistance']=='far','TV viewing distance must be far'); req('directional' in data['formFactor']['tv']['primaryInput'],'TV primary input must be directional')
    css=text('css/glaze.formfactors.css')
    for m in ('.glaze-mobile-shell','.glaze-tablet-shell','.glaze-desktop-shell','.glaze-tv-shell','.glaze-tv-focusable','--glaze-tv-safe-inline','--glaze-tv-safe-block','prefers-reduced-motion','forced-colors'): req(m in css,f'form-factor CSS missing {m}')
    contract=text('FORM_FACTORS.md')
    for m in ('Mobile UI','Tablet UI','Desktop UI','TV UI','TV is defined primarily by far viewing distance','TV must never be treated as Wide Desktop'): req(m in contract,f'FORM_FACTORS.md missing {m}')
    ref=text('reference/formfactors.html')
    for m in ('data-profile="mobile"','data-profile="tablet"','data-profile="desktop"','data-profile="tv"','ArrowLeft','ArrowRight','ArrowUp','ArrowDown'): req(m in ref,f'form-factor reference missing {m}')
    acceptance=text('ACCEPTANCE.md')
    for m in ('390 × 844','820 × 1180','1280 × 900','1600 × 1000','1920 × 1080','directional focus','overscan-safe'): req(m in acceptance,f'acceptance missing {m}')
    readme=text('README.md')
    req('Glaze UI 1.4.0 is the current Stable canonical baseline' in readme,'README Stable statement missing')
    req('dependency-free five-profile reference' in readme,'README must describe the five-profile Stable form-factor reference')
    req('dependency-free four-profile reference' not in readme,'README contains stale four-profile form-factor wording')
    for m in ('Mobile 390×844','Tablet 820×1180','Desktop 1280×900','Wide Desktop 1600×1000','TV 1920×1080'):
        req(m in readme,f'README Stable form-factor matrix missing {m}')
    req('Glaze UI 1.4 Stable form-factor layer' in text('COMPONENT_STATUS.md'),'lifecycle promotion missing'); req('Stable baseline:** Glaze UI **1.4.0' in text('STABILITY.md'),'stability baseline missing'); req(json.loads(text('consumers/registry.json'))['stableBaseline']=='1.4.0','consumer baseline missing'); req('Glaze UI 1.4 Stable' in text('website/index.html'),'public site Stable marker missing')
    print('Glaze UI 1.4 Stable form-factor source validation passed')
if __name__=='__main__': main()

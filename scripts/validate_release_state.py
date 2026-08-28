#!/usr/bin/env python3
"""Fail closed when Glaze UI Stable release-state or mandatory consumer records drift."""
from __future__ import annotations
import json,re
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
VERSION=(ROOT/'VERSION').read_text(encoding='utf-8').strip()
def require(c,m):
    if not c: raise SystemExit(f'Glaze UI release-state validation failed: {m}')
def text(p): return (ROOT/p).read_text(encoding='utf-8')
def main():
    require(re.fullmatch(r'\d+\.\d+\.\d+',VERSION) is not None,'VERSION must use semantic versioning')
    require(VERSION=='2.0.0','current Stable VERSION must be 2.0.0')
    tokens=json.loads(text('tokens/glaze.tokens.json'))
    require(tokens['meta']['version']==VERSION and tokens['meta']['status']=='Stable','canonical tokens must match 2.0 Stable VERSION')
    require(tokens['meta']['stableBaseline']==VERSION,'canonical Stable baseline differs from VERSION')
    require(tokens['meta'].get('governingSentence')=='Make interaction feel tangible.','governing sentence missing')
    current=tokens.get('currentContract',{})
    require(current.get('major')==2,'current contract major must be 2')
    require(current.get('materialLevels')==['Canvas','Surface','Soft Glaze','Glaze','Deep Glaze','Live Glaze'],'current material hierarchy drifted')
    require(current.get('touchMinimum')==48 and current.get('tvMinimum')==56,'2.0 target floors drifted')
    for k in ('connectedTransformation','foldableFirstClass','wearableRotationalNavigation','spatialFloatingSurfaces','advancedEffectsOptional'):
        require(current.get(k) is True,f'current Stable invariant missing: {k}')
    require(current.get('presentationCreatesDomainTruth') is False,'Glaze presentation must not create domain truth')

    registry=json.loads(text('consumers/registry.json'))
    require(registry.get('schemaVersion')==3,'consumer registry schema must be 3')
    require(registry.get('stableBaseline')==VERSION and registry.get('requiredConsumerVersion')==VERSION,'consumer Stable target differs from VERSION')
    require('1.6.0' in registry.get('historicalStableVersions',[]),'1.6.0 must be historical after 2.0 promotion')
    require(registry.get('enforcement',{}).get('currentStableRequired') is True,'current Stable consumer requirement missing')
    require(registry.get('enforcement',{}).get('productionExceptionsAllowed') is False,'production exceptions must remain forbidden')
    for repo in ('GoreeCloud/goreecloud-launcher','GoreeCloud/goreecloud-keyboard'):
        matches=[c for c in registry.get('consumers',[]) if c.get('repository')==repo]
        require(len(matches)==1,f'{repo} registry record missing/duplicate')
        entry=matches[0]
        require(entry.get('status')=='migration-required' and entry.get('targetVersion')=='1.6.0',f'{repo} must preserve 1.6 evidence as migration-required')
        require(entry.get('requiredTargetVersion')==VERSION and entry.get('productionEligible') is False,f'{repo} current Stable migration boundary drifted')

    enforcement=json.loads(text('tokens/enforcement.json'))
    require(enforcement.get('meta',{}).get('currentStable')==VERSION,'enforcement current Stable differs from VERSION')

    candidate=json.loads(text('tokens/glaze-2.candidate.json')); meta=candidate.get('meta',{})
    require(meta.get('version')=='2.0.0' and meta.get('status')=='Candidate','promotion-source Candidate snapshot drifted')
    require(meta.get('stableImplementationBaseline')=='1.6.0','Candidate snapshot previous Stable baseline drifted')
    require(meta.get('productionEligible') is False and meta.get('requiresStablePromotion') is True,'Candidate snapshot must preserve pre-promotion lifecycle evidence')

    readme=text('README.md'); stability=text('STABILITY.md'); identity=text('IDENTITY.md'); status=text('COMPONENT_STATUS.md'); components=text('COMPONENTS.md'); conformance=text('CONFORMANCE.md'); acceptance=text('ACCEPTANCE.md'); adoption=text('ADOPTION.md'); consumers=text('CONSUMERS.md'); stable=text('GLAZE_UI_2_STABLE.md')
    require(f'Glaze UI {VERSION} is the current Stable canonical baseline' in readme,'README current Stable declaration missing')
    require(f'**Stable baseline:** Glaze UI **{VERSION}**' in stability,'STABILITY current Stable declaration missing')
    require(f'Glaze UI {VERSION} is the current Stable GoreeCloud design-system baseline' in identity,'IDENTITY current Stable declaration missing')
    require('Glaze UI 2.0 Stable systems' in status,'2.0 Stable lifecycle section missing')
    require(components.startswith('# Glaze UI 2.0 Component Contract\n'),'2.0 component contract heading missing')
    require(f'Glaze UI **{VERSION}** is the current Stable baseline' in conformance,'CONFORMANCE current Stable declaration missing')
    require(f'Glaze UI {VERSION} is the current Stable baseline' in adoption,'ADOPTION current Stable declaration missing')
    require(f'Glaze UI **{VERSION}** is the current Stable baseline' in consumers,'CONSUMERS current Stable declaration missing')
    require('# Glaze UI 2.0 — Enforced Stable Design Contract' in stable,'2.0 Stable release contract missing')
    require('Lifecycle status:** Stable' in stable and 'Previous Stable implementation baseline:** Glaze UI 1.6.0' in stable,'2.0 Stable lifecycle/rollback boundary missing')
    require('Canvas / Surface / Soft Glaze / Glaze / Deep Glaze / Live Glaze' in acceptance,'current acceptance material hierarchy missing')
    require('2.0 Stable promotion acceptance' in acceptance,'2.0 Stable promotion gate missing')
    require('No downstream application is promoted by declaration' in stability,'downstream application boundary missing')
    require('No production exception' in consumers,'no-exception consumer rule missing')
    require('application-specific native or real-device acceptance' in conformance,'consumer native/real-device boundary missing')
    require('legacy 1.x compatibility' in components,'legacy compatibility boundary missing')
    require('Glaze Motion' in status and 'Experimental' in status,'Glaze Motion must remain non-Stable')
    print(f'Glaze UI release-state validation passed for {VERSION}; 2.0 Stable consumer enforcement active')
if __name__=='__main__': main()

#!/usr/bin/env python3
"""Fail closed when Glaze UI Stable release-state or mandatory consumer records drift."""
from __future__ import annotations
import json,re
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
VERSION=(ROOT/'VERSION').read_text(encoding='utf-8').strip()
LAUNCHER='GoreeCloud/goreecloud-launcher'; LAUNCHER_ADOPTION='88e7007013ac096a39f04ff4a3993591ef2ed5f2'
KEYBOARD='GoreeCloud/goreecloud-keyboard'; KEYBOARD_ADOPTION='3c82fff63d328bcc5f375b1b5a9bf9b692cd8c73'
def require(c,m):
    if not c: raise SystemExit(f'Glaze UI release-state validation failed: {m}')
def text(p): return (ROOT/p).read_text(encoding='utf-8')
def by_repo(registry,repo):
    matches=[c for c in registry.get('consumers',[]) if c.get('repository')==repo]
    require(len(matches)==1,f'{repo} registry record missing/duplicate')
    return matches[0]
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
    require(registry.get('schemaVersion')==4,'consumer registry schema must be 4')
    require(registry.get('stableBaseline')==VERSION and registry.get('requiredConsumerVersion')==VERSION,'consumer Stable target differs from VERSION')
    require('1.6.0' in registry.get('historicalStableVersions',[]),'1.6.0 must be historical after 2.0 promotion')
    require(registry.get('enforcement',{}).get('currentStableRequired') is True,'current Stable consumer requirement missing')
    require(registry.get('enforcement',{}).get('productionExceptionsAllowed') is False,'production exceptions must remain forbidden')

    lifecycle=json.loads(text('registry/lifecycle.json'))
    active_candidate=lifecycle.get('activeCandidate')
    require(active_candidate=='2.1.0-candidate.1','active Candidate must remain 2.1.0-candidate.1 during this tranche')
    candidate_release=[r for r in lifecycle.get('releases',[]) if isinstance(r,dict) and r.get('version')==active_candidate]
    require(len(candidate_release)==1 and candidate_release[0].get('status')=='candidate','active Candidate release record missing/invalid')
    require(candidate_release[0].get('consumerEligible') is False,'active Candidate release must remain non-consumer-eligible')
    promotion=lifecycle.get('promotionRules',{})
    require(promotion.get('candidateMaySatisfyStableConsumerConformance') is False,'Candidate must not satisfy Stable consumer conformance')
    require(promotion.get('stableVersionFileMustRemain')==VERSION,'Candidate work must preserve current Stable VERSION')

    assessment=registry.get('candidateAssessment',{})
    require(assessment.get('version')==active_candidate,'consumer Candidate assessment must track lifecycle activeCandidate')
    require(assessment.get('lifecycle')=='candidate','consumer Candidate assessment lifecycle must remain Candidate')
    require(assessment.get('consumerEligible') is False,'consumer Candidate assessment must remain non-consumer-eligible')
    require(assessment.get('productionEligible') is False,'consumer Candidate assessment must remain non-production')
    evaluations=assessment.get('evaluations')
    require(isinstance(evaluations,list),'consumer Candidate evaluations must be a list')
    for item in evaluations:
        require(isinstance(item,dict),'consumer Candidate evaluation must be an object')
        require(item.get('targetVersion')==active_candidate,'consumer Candidate evaluation target must equal activeCandidate')
        require(item.get('productionEligible') is False,'consumer Candidate evaluation must remain non-production')
        require(item.get('stableConformanceUnaffected') is True,'consumer Candidate evaluation must not rewrite Stable conformance')

    launcher=by_repo(registry,LAUNCHER)
    require(launcher.get('status')=='adoption-candidate' and launcher.get('targetVersion')==VERSION,'Launcher must remain a 2.0 Adoption Candidate during final application acceptance')
    require(launcher.get('requiredTargetVersion')==VERSION and launcher.get('productionEligible') is False,'Launcher 2.0 Adoption Candidate production boundary drifted')
    require(launcher.get('referenceRevision')==LAUNCHER_ADOPTION and launcher.get('evidence')=='docs/glaze-ui-adoption.md','Launcher current adoption evidence anchor drifted')
    require(launcher.get('automatedContract') is True,'Launcher current adoption must remain automated')

    keyboard=by_repo(registry,KEYBOARD)
    require(keyboard.get('status')=='migration-required' and keyboard.get('targetVersion')=='1.6.0','Keyboard must preserve 1.6 evidence as migration-required')
    require(keyboard.get('requiredTargetVersion')==VERSION and keyboard.get('productionEligible') is False,'Keyboard current Stable migration boundary drifted')
    require(keyboard.get('referenceRevision')==KEYBOARD_ADOPTION and keyboard.get('evidence')=='docs/glaze-ui-adoption.md','Keyboard historical adoption evidence anchor drifted')
    require(keyboard.get('automatedContract') is True,'Keyboard historical adoption evidence must remain automated')

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
    print(f'Glaze UI release-state validation passed for {VERSION}; schema 4 Stable audit preserved and {active_candidate} remains non-consumer-eligible')
if __name__=='__main__': main()

#!/usr/bin/env python3
"""Fail-closed governance validation for Glaze Motion 0.6 Experimental under Glaze UI 2.1 Stable."""
from __future__ import annotations
import json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
TOKENS=ROOT/'tokens/glaze-motion.json'; DOC=ROOT/'GLAZE_MOTION.md'; NATIVE=ROOT/'NATIVE_MOTION_MAPPINGS.md'; CSS=ROOT/'css/glaze.motion.core.css'; RUNTIME=ROOT/'js/glaze.motion.js'; ACCESSIBILITY=ROOT/'js/glaze.motion.accessibility.js'; CORE=ROOT/'js/glaze.motion.core.js'; ACCEPTANCE=ROOT/'acceptance/glaze-motion-0.6-experimental.md'; REGISTRY=ROOT/'consumers'/'registry.json'; REFERENCE=ROOT/'reference/glaze-motion.html'; RENDERED=ROOT/'scripts/validate_glaze_motion_rendered.py'
LAUNCHER='GoreeCloud/goreecloud-launcher'; KEYBOARD='GoreeCloud/goreecloud-keyboard'; LAUNCHER_HEAD='3095b9320b660f5e166465990d5d2bee061d7422'; LAUNCHER_MERGE='23a389b3b24db726ceab5e328f9f8157fa7655ae'; LAUNCHER_ADOPTION='88e7007013ac096a39f04ff4a3993591ef2ed5f2'; KEYBOARD_HEAD='80de7bd2dcff6d07b06b19f8250e37d20155d7ff'; KEYBOARD_MERGE='c9c0500263b40640339cf7a46f1a029d9a2ac240'; KEYBOARD_ADOPTION='3c82fff63d328bcc5f375b1b5a9bf9b692cd8c73'
def req(c,m):
    if not c: raise SystemExit(f'Glaze Motion validation failed: {m}')
def phrases(body,items,label):
    for item in items: req(item in body,f'{label} missing: {item}')
def by_repo(entries,repo):
    found=[x for x in entries if x.get('repository')==repo]; req(len(found)==1,f'exactly one record required for {repo}'); return found[0]
def main():
    required=(TOKENS,DOC,NATIVE,CSS,RUNTIME,ACCESSIBILITY,CORE,ACCEPTANCE,REGISTRY,REFERENCE,RENDERED,ROOT/'tests/glaze-motion-runtime.test.mjs',ROOT/'tests/glaze-motion-interaction.test.mjs',ROOT/'tests/glaze-motion-accessibility.test.mjs',ROOT/'tests/glaze-motion-consumer.test.mjs')
    for p in required: req(p.is_file(),f'missing {p.relative_to(ROOT)}')
    data=json.loads(TOKENS.read_text()); meta=data.get('glazeMotion',{})
    req(meta.get('version')=='0.6.0' and meta.get('status')=='experimental','Glaze Motion 0.6 must remain Experimental')
    req(meta.get('extendsGlazeUi')=='1.5.0','historical Motion evaluation baseline changed')
    req(meta.get('runtimeCompatibilityBaseline')=='0.4.0','runtime compatibility baseline changed')
    tiers=data.get('tiers',{}); req(tiers.get('core',{}).get('status')=='experimental','Motion Core must remain Experimental'); req(tiers.get('studio',{}).get('status')=='planned','Motion Studio must remain Planned'); req(tiers.get('spatial',{}).get('status')=='planned','Motion Spatial must remain Planned')
    req(data.get('durationsMs')=={'instant':0,'micro':90,'short':160,'medium':240,'long':360,'ambient':700},'duration roles changed')
    for name,spring in data.get('springs',{}).items(): req(spring.get('mass',0)>0 and spring.get('stiffness',0)>0 and spring.get('damping',0)>0,f'{name} spring invalid'); req(0<=spring.get('maxOvershoot',1)<=0.1,f'{name} overshoot unbounded')
    gestures=data.get('gestures',{}); req(gestures.get('slopPx')==4 and gestures.get('velocityWindowMs')==120 and gestures.get('swipeThresholdRatio')==0.33,'gesture thresholds changed'); req(gestures.get('directManipulationSurvivesReducedMotion') is True and gestures.get('settlingMotionCollapsesUnderReducedMotion') is True,'reduced-motion gesture invariants changed'); req(gestures.get('keyboardAndRemoteAlternativesRequired') is True and gestures.get('semanticResultIndependentOfInputModality') is True,'input parity changed')
    accessible=data.get('accessibleInteraction',{}); req(accessible.get('reorderRequiresStableKeys') is True,'stable-key reorder contract missing'); req(accessible.get('directionalMoveOrientations')==['vertical','horizontal'],'directional mapping changed'); req(accessible.get('hardCodedAnnouncementCopyProhibited') is True and accessible.get('localizationOwnedByConsumer') is True,'accessible localization boundary changed')
    perf=data.get('performance',{}); req(perf.get('targetFps')==60 and perf.get('frameBudgetMs',99)<=16.7 and perf.get('maxLongTaskMs',99)<=50,'performance budget weakened'); req(perf.get('persistentWillChangeForCoreUi') is False,'persistent will-change prohibited'); req(perf.get('instrumentation',{}).get('localOnly') is True and perf.get('instrumentation',{}).get('networkReporting') is False,'performance evidence must remain local-only')
    native=data.get('nativeMappings',{}); req(native.get('requiredForCandidatePromotion') is True and native.get('semanticParityRequired') is True,'native mapping promotion boundary changed')
    evidence=data.get('consumerEvidence',{}); req(evidence.get('productionConsumerCertification') is False,'reference evidence cannot certify production consumers'); evaluations=evidence.get('firstPartyEvaluations'); req(isinstance(evaluations,list) and len(evaluations)==2,'exactly two governed first-party evaluations required')
    for repo,name,motion,pr,head,merge,ci in ((LAUNCHER,'GoreeCloud Launcher','0.4.0',22,LAUNCHER_HEAD,LAUNCHER_MERGE,67),(KEYBOARD,'GoreeCloud Keyboard','0.5.0',4,KEYBOARD_HEAD,KEYBOARD_MERGE,15)):
        e=by_repo(evaluations,repo); req(e.get('consumer')==name and e.get('consumerState')=='adoption-candidate','historical evaluation state changed'); req(e.get('targetGlazeUi')=='1.5.0' and e.get('evaluatedMotionVersion')==motion,'historical evaluation target changed'); req(e.get('pullRequest')==pr and e.get('validatedHead')==head and e.get('mergeRevision')==merge and e.get('ciRun')==ci,'exact evaluation evidence changed'); req(e.get('evaluationMode')=='native-android-test-only' and e.get('productionDependency') is False and e.get('nativeDeviceCertification') is False and e.get('candidatePromotionSufficient') is False,'experimental evidence boundary changed')
    reduced=data.get('reducedMotion',{}); req(reduced.get('required') is True and reduced.get('durationMs')==0 and reduced.get('preserveDirectManipulationTracking') is True and reduced.get('removePostGestureInertia') is True,'reduced-motion invariants changed')
    req(data.get('authority',{})=={'presentation':'Glaze UI / Glaze Motion','privacyTruth':'Privacy Shield','securityTruth':'Wardveil Security','resilienceTruth':'Everkeep','coordinationTruth':'GoreeCloud Mesh'},'authority mapping changed')

    # Glaze Motion remains Experimental across Stable Glaze UI promotions. The two
    # native evaluations below are historical Motion evidence, while the canonical
    # consumer registry must reflect the current Stable 2.1 migration boundary.
    version=(ROOT/'VERSION').read_text().strip(); req(version=='2.1.0','Glaze Motion governance expects current Stable Glaze UI 2.1.0')
    registry=json.loads(REGISTRY.read_text()); req(registry.get('stableBaseline')==version and registry.get('requiredConsumerVersion')==version,'consumer Stable baseline differs from VERSION')
    launcher=by_repo(registry.get('consumers',[]),LAUNCHER)
    req(launcher.get('status')=='migration-required','Launcher must be migration-required after Glaze UI 2.1 Stable promotion')
    req(launcher.get('targetVersion')=='2.0.0' and launcher.get('requiredTargetVersion')=='2.1.0','Launcher must preserve 2.0 evidence while requiring current Stable 2.1.0')
    req(launcher.get('referenceRevision')==LAUNCHER_ADOPTION and launcher.get('evidence')=='docs/glaze-ui-adoption.md','Launcher historical adoption evidence changed')
    req(launcher.get('automatedContract') is True and launcher.get('productionEligible') is False,'Launcher production boundary changed')

    keyboard=by_repo(registry.get('consumers',[]),KEYBOARD)
    req(keyboard.get('status')=='migration-required','Keyboard must remain migration-required until its own 2.1 adoption exists')
    req(keyboard.get('targetVersion')=='1.6.0' and keyboard.get('requiredTargetVersion')=='2.1.0','Keyboard must preserve 1.6 evidence while requiring 2.1')
    req(keyboard.get('referenceRevision')==KEYBOARD_ADOPTION and keyboard.get('evidence')=='docs/glaze-ui-adoption.md','Keyboard adoption evidence changed')
    req(keyboard.get('automatedContract') is True and keyboard.get('productionEligible') is False,'Keyboard production boundary changed')

    doc=DOC.read_text(); phrases(doc,('Experimental foundation (0.6.0)','Runtime implementation baseline','Direct manipulation and accessible gestures','settling budget','Native mappings','First-party downstream evidence','GoreeCloud Launcher','GoreeCloud Keyboard','Rendered acceptance','Motion Studio — Planned','Motion Spatial — Planned','two test-only native Android evaluations are still insufficient'),'GLAZE_MOTION.md'); req(LAUNCHER_HEAD in doc and LAUNCHER_MERGE in doc and KEYBOARD_HEAD in doc and KEYBOARD_MERGE in doc,'Motion documentation missing exact historical consumer evaluation evidence')
    native_doc=NATIVE.read_text(); phrases(native_doc,('Mobile and tablet native','Desktop native','TV native','First-party native evaluation evidence','Performance evidence','Authority boundary','Settings.Global.ANIMATOR_DURATION_SCALE'),'native mapping guidance')
    acceptance=ACCEPTANCE.read_text(); phrases(acceptance,('Experimental evidence/governance iteration','First-party downstream evidence','What 0.6 does not prove','Runtime compatibility boundary','Promotion boundary','This evidence remains insufficient for Candidate promotion.'),'0.6 acceptance')
    css=CSS.read_text(); req('Glaze Motion 0.3 Experimental' in css and '@media (prefers-reduced-motion: reduce)' in css,'retained Motion CSS markers missing'); req('will-change:' not in css,'persistent will-change prohibited')
    runtime=RUNTIME.read_text(); phrases(runtime,('GLAZE_MOTION_VERSION = "0.3.0"','createReorderModel','resolveSwipeAction','resolveDirectionalMove','createPanZoomState','createFrameBudgetProbe','createDragSession','startSharedTransition'),'compatibility runtime')
    acc=ACCESSIBILITY.read_text(); phrases(acc,('GLAZE_MOTION_ACCESSIBILITY_VERSION = "0.4.0"','resolveReorderCommand','createAccessibleReorderController','createSettlingBudget','reason: "reduced-motion"','reason: "budget-exhausted"'),'accessibility runtime'); req('announcement:' not in acc,'runtime must not hard-code localized announcement copy')
    core=CORE.read_text(); phrases(core,('export * from "./glaze.motion.js"','export * from "./glaze.motion.accessibility.js"'),'aggregate runtime')
    print('Glaze Motion 0.6 Experimental validated under Glaze UI 2.1 Stable: historical evaluations preserved; Launcher and Keyboard require 2.1 migration; Motion remains non-production')
if __name__=='__main__': main()

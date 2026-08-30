#!/usr/bin/env python3
"""Fail-closed structural validation for Glaze UI 2.1 reference, resilience and screenshot-capture staging."""
from __future__ import annotations
import json,pathlib,sys
ROOT=pathlib.Path(__file__).resolve().parents[1];ERRORS=[]
def fail(m):ERRORS.append(m)
def read_text(p):
 t=ROOT/p
 if not t.is_file():fail(f"missing required file: {p}");return ""
 return t.read_text(encoding="utf-8")
def read_json(p):
 raw=read_text(p)
 if not raw:return {}
 try:v=json.loads(raw)
 except json.JSONDecodeError as e:fail(f"invalid JSON in {p}: {e}");return {}
 if not isinstance(v,dict):fail(f"top level must be an object: {p}");return {}
 return v

def main():
 if read_text("VERSION").strip()!="2.0.0":fail("Glaze UI 2.1 Candidate regression must not change Stable VERSION from 2.0.0")
 contract=read_json("contracts/regression/reference-invariants.json");manifest=read_json("contracts/regression/visual-baselines.json");registry=read_json("registry/lifecycle.json");workflow=read_text(".github/workflows/glaze-2.1-candidate.yml");css=read_text("css/glaze-2.1.expanded-reference.css");base_css=read_text("css/glaze-2.1.reference.css");resilience_css=read_text("css/glaze-2.1.resilience-reference.css");snapshot=read_text("reference/candidate-2.1-snapshot.html")
 if contract.get("lifecycle")!="candidate":fail("reference regression contract must remain Candidate")
 if contract.get("scope")!="computed-layout-style-and-interaction-invariants":fail("reference regression scope must remain computed layout/style/interaction invariants")
 if contract.get("pixelBaselineStatus")!="capture-required":fail("pixel baseline status must remain capture-required until reviewed baseline PNGs are committed and compared")
 expected={"settings-preferences":("reference/candidate-2.1-settings.html","productivity"),"file-management":("reference/candidate-2.1-files.html","productivity"),"search-command":("reference/candidate-2.1-search.html","productivity"),"communication-live-activity":("reference/candidate-2.1-communication.html","communication"),"media-playback":("reference/candidate-2.1-media.html","media"),"resilience-exception-states":("reference/candidate-2.1-resilience.html","administration")};flows=contract.get("flows",{});combined=""
 if set(flows)!=set(expected):fail(f"regression contract flow set must be exactly {sorted(expected)}")
 for marker,(path,recipe) in expected.items():
  record=flows.get(marker,{})
  if record.get("path")!=path:fail(f"{marker} path must be {path}")
  if record.get("recipe")!=recipe:fail(f"{marker} recipe must be {recipe}")
  baseline=record.get("visualBaseline")
  if not isinstance(baseline,str) or not baseline.endswith("-v1"):fail(f"{marker} must define a v1 visual baseline identifier")
  page=read_text(path);combined+="\n"+page
  if f'data-reference-flow="{marker}"' not in page:fail(f"{path} missing canonical flow marker {marker}")
  if marker in {"search-command","communication-live-activity","media-playback","resilience-exception-states"}:
   if f'data-visual-baseline="{baseline}"' not in page:fail(f"{path} missing declared visual baseline {baseline}")
   if "measureVisibleMaterialBudget" not in page or "applyReferenceRuntime" not in page:fail(f"{path} must execute shared 2.1 runtime and Material Budget")
  for state in record.get("requiredStates",[]):
   if f'data-regression-state="{state}"' not in page:fail(f"{path} missing required regression state {state}")
 vocab=set(contract.get("stateVocabulary",[]));required={"default","hover","focus","pressed","selected","disabled","loading","sending","success","warning","error","offline","protected","restricted","empty","unavailable","conflict","expired","destructive","degraded"}
 if not required.issubset(vocab):fail(f"state vocabulary missing {sorted(required-vocab)}")
 for state in ("loading","sending","success","warning","error","offline","protected","restricted","empty","unavailable","conflict","expired","destructive","degraded"):
  if f'data-regression-state="{state}"' not in combined:fail(f"expanded reference flows do not visibly exercise state {state}")
 for selector in (":hover",":focus-visible",":active",":disabled",'[aria-current="page"]','[aria-pressed="true"]'):
  if selector not in css and selector not in base_css:fail(f"reference CSS missing state selector {selector}")
 for marker in (".exception-grid",'data-regression-state="conflict"','data-regression-state="destructive"',"@media(forced-colors:active)"):
  if marker not in resilience_css:fail(f"resilience CSS missing marker: {marker}")
 scenarios=contract.get("interactionScenarios",[]);sm={i.get("id"):i for i in scenarios if isinstance(i,dict)};expected_s={"command-open-select":"search-command","message-send":"communication-live-activity","playback-toggle":"media-playback"}
 if set(sm)!=set(expected_s):fail(f"interaction scenarios must remain exactly {sorted(expected_s)}")
 for scenario,flow in expected_s.items():
  if sm.get(scenario,{}).get("flow")!=flow:fail(f"{scenario} must target {flow}")
  if not isinstance(sm.get(scenario,{}).get("trigger"),str) or not sm.get(scenario,{}).get("trigger"):fail(f"{scenario} must declare a trigger selector")
 if not isinstance(contract.get("visualInvariants"),list) or len(contract.get("visualInvariants",[]))<10:fail("reference regression contract must define at least ten visual invariants")
 caps=registry.get("capabilities",{});ref=caps.get("canonical-reference-flows-2.1",{});coverage=set(ref.get("coverage",[]));implementations=set(ref.get("implementations",[]))
 if not set(expected).issubset(coverage):fail(f"lifecycle registry reference-flow coverage missing {sorted(set(expected)-coverage)}")
 for path,_ in expected.values():
  if path not in implementations:fail(f"lifecycle registry missing reference implementation {path}")
 expanded=caps.get("expanded-acceptance-matrix-2.1",{});interaction=caps.get("interaction-regression-2.1",{});visual=caps.get("rendered-visual-invariant-regression-2.1",{});pixel=caps.get("visual-regression-2.1",{})
 if expanded.get("status")!="candidate" or expanded.get("implementation")!="contracts/regression/reference-invariants.json":fail("expanded acceptance matrix must be Candidate and point to regression contract")
 if expanded.get("resilienceAcceptance")!="scripts/validate_glaze_2_1_resilience_rendered.py":fail("expanded acceptance matrix must point to resilience rendered acceptance")
 if interaction.get("status")!="candidate" or interaction.get("implementation")!="reference/candidate-2.1-expanded-acceptance.html":fail("interaction regression must remain Candidate and point to expanded rendered harness")
 if visual.get("status")!="candidate" or visual.get("implementation")!="contracts/regression/reference-invariants.json":fail("rendered visual-invariant regression must remain Candidate")
 if visual.get("resilienceAcceptance")!="scripts/validate_glaze_2_1_resilience_rendered.py":fail("rendered visual-invariant regression must point to resilience acceptance")
 if pixel.get("status")!="planned":fail("screenshot visual regression must remain Planned before reviewed baseline PNGs exist")
 for key,value in (("manifest","contracts/regression/visual-baselines.json"),("captureImplementation","scripts/glaze_2_1_visual_regression.py"),("snapshotHarness","reference/candidate-2.1-snapshot.html")):
  if pixel.get(key)!=value:fail(f"visual-regression-2.1 {key} must be {value}")
 if manifest.get("lifecycle")!="planned" or manifest.get("status")!="capture-required" or manifest.get("baselineRevision") is not None:fail("visual baseline manifest must remain Planned/capture-required with null baselineRevision before baseline acceptance")
 thresholds=manifest.get("thresholds",{})
 if not isinstance(thresholds.get("perChannelTolerance"),int) or not 0<=thresholds.get("perChannelTolerance",-1)<=32:fail("visual per-channel tolerance must be an integer from 0 to 32")
 if not isinstance(thresholds.get("maxChangedPixelRatio"),(int,float)) or not 0<thresholds.get("maxChangedPixelRatio",0)<=0.02:fail("visual changed-pixel ratio must be >0 and <=2%")
 if not isinstance(thresholds.get("maxMeanAbsoluteChannelDelta"),(int,float)) or not 0<thresholds.get("maxMeanAbsoluteChannelDelta",0)<=4:fail("visual mean channel delta must be >0 and <=4")
 expected_cases={"settings-desktop-light","files-mobile-reduced-transparency","search-command-open-deep-dark","communication-tablet-sent-large-text","media-tv-playing","resilience-desktop-light"};cases=manifest.get("cases",[]);case_map={c.get("id"):c for c in cases if isinstance(c,dict)}
 if set(case_map)!=expected_cases:fail(f"visual baseline manifest case set must be exactly {sorted(expected_cases)}")
 for cid,case in case_map.items():
  if case.get("flow") not in {"settings","files","search","communication","media","resilience"}:fail(f"visual case {cid} has invalid flow")
  if not isinstance(case.get("width"),int) or not isinstance(case.get("height"),int) or case.get("width",0)<320 or case.get("height",0)<640:fail(f"visual case {cid} has invalid viewport")
  if not isinstance(case.get("baseline"),str) or not case.get("baseline","").startswith("reference/baselines/2.1/") or not case.get("baseline","").endswith(".png"):fail(f"visual case {cid} has invalid baseline path")
  if not (ROOT/case.get("path","")).is_file():fail(f"visual case {cid} target path is missing: {case.get('path')}")
 for marker in ('data-snapshot-ready="pending"',"command-open","message-sent","playing","candidate-2.1-resilience.html"):
  if marker not in snapshot:fail(f"snapshot harness missing marker: {marker}")
 for marker in ("scripts/validate_glaze_2_1_regression.py","scripts/validate_glaze_2_1_expanded_rendered.py","scripts/validate_glaze_2_1_resilience_rendered.py","scripts/glaze_2_1_visual_regression.py","capture --output-dir","actions/upload-artifact@ea165f8d65b6e75b540449e92b4886f43607fa02"):
  if marker not in workflow:fail(f"2.1 workflow missing screenshot/resilience marker: {marker}")
 if "reference/candidate-2.1-expanded-acceptance.html" not in read_text("scripts/validate_glaze_2_1_expanded_rendered.py"):fail("expanded rendered validator must invoke expanded acceptance harness")
 if "reference/candidate-2.1-resilience-acceptance.html" not in read_text("scripts/validate_glaze_2_1_resilience_rendered.py"):fail("resilience validator must invoke resilience acceptance harness")
 visual_script=read_text("scripts/glaze_2_1_visual_regression.py")
 for marker in ("decode_png","compare_case","--force-device-scale-factor=1",'data-snapshot-ready="true"'):
  if marker not in visual_script:fail(f"visual regression script missing marker: {marker}")
 if ERRORS:
  print("Glaze UI 2.1 expanded regression validation FAILED",file=sys.stderr)
  for e in ERRORS:print(f"- {e}",file=sys.stderr)
  return 1
 print("Glaze UI 2.1 expanded regression and screenshot-capture staging validation passed; Stable remains 2.0.0")
 print("Screenshot PNGs are capture candidates only until reviewed, committed as baselines, and a fresh exact-head pixel comparison succeeds.")
 return 0
if __name__=="__main__":raise SystemExit(main())

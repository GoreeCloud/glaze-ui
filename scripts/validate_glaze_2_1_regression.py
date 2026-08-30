#!/usr/bin/env python3
"""Fail-closed structural validation for Glaze UI 2.1 expanded reference regression."""
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
 if read_text("VERSION").strip()!="2.0.0":fail("expanded 2.1 Candidate regression must not change Stable VERSION from 2.0.0")
 contract=read_json("contracts/regression/reference-invariants.json");registry=read_json("registry/lifecycle.json");workflow=read_text(".github/workflows/glaze-2.1-candidate.yml");css=read_text("css/glaze-2.1.expanded-reference.css");base_css=read_text("css/glaze-2.1.reference.css")
 if contract.get("lifecycle")!="candidate":fail("reference regression contract must remain Candidate")
 if contract.get("scope")!="computed-layout-style-and-interaction-invariants":fail("reference regression scope must remain computed layout/style/interaction invariants")
 if contract.get("pixelBaselineStatus")!="planned":fail("pixel screenshot baseline diffing must remain Planned until real baseline evidence exists")
 expected={"settings-preferences":("reference/candidate-2.1-settings.html","productivity"),"file-management":("reference/candidate-2.1-files.html","productivity"),"search-command":("reference/candidate-2.1-search.html","productivity"),"communication-live-activity":("reference/candidate-2.1-communication.html","communication"),"media-playback":("reference/candidate-2.1-media.html","media")};flows=contract.get("flows",{});combined=""
 if set(flows)!=set(expected):fail(f"regression contract flow set must be exactly {sorted(expected)}")
 for marker,(path,recipe) in expected.items():
  record=flows.get(marker,{})
  if record.get("path")!=path:fail(f"{marker} path must be {path}")
  if record.get("recipe")!=recipe:fail(f"{marker} recipe must be {recipe}")
  baseline=record.get("visualBaseline")
  if not isinstance(baseline,str) or not baseline.endswith("-v1"):fail(f"{marker} must define a v1 visual baseline identifier")
  page=read_text(path);combined+="\n"+page
  if f'data-reference-flow="{marker}"' not in page:fail(f"{path} missing canonical flow marker {marker}")
  if path.endswith(("search.html","communication.html","media.html")):
   if f'data-visual-baseline="{baseline}"' not in page:fail(f"{path} missing declared visual baseline {baseline}")
   if "measureVisibleMaterialBudget" not in page or "applyReferenceRuntime" not in page:fail(f"{path} must execute the shared 2.1 runtime and Material Budget")
  for state in record.get("requiredStates",[]):
   if f'data-regression-state="{state}"' not in page:fail(f"{path} missing required regression state {state}")
 vocab=set(contract.get("stateVocabulary",[]));required={"default","hover","focus","pressed","selected","disabled","loading","sending","success","warning","error","offline","protected","restricted"}
 if not required.issubset(vocab):fail(f"state vocabulary missing {sorted(required-vocab)}")
 for state in ("loading","sending","success","warning","error","offline","protected","restricted"):
  if f'data-regression-state="{state}"' not in combined:fail(f"expanded reference flows do not visibly exercise state {state}")
 for selector in (":hover",":focus-visible",":active",":disabled",'[aria-current="page"]','[aria-pressed="true"]'):
  if selector not in css and selector not in base_css:fail(f"reference CSS missing state selector {selector}")
 scenarios=contract.get("interactionScenarios",[]);sm={i.get("id"):i for i in scenarios if isinstance(i,dict)};expected_s={"command-open-select":"search-command","message-send":"communication-live-activity","playback-toggle":"media-playback"}
 if set(sm)!=set(expected_s):fail(f"interaction scenarios must be exactly {sorted(expected_s)}")
 for scenario,flow in expected_s.items():
  if sm.get(scenario,{}).get("flow")!=flow:fail(f"{scenario} must target {flow}")
  if not isinstance(sm.get(scenario,{}).get("trigger"),str) or not sm.get(scenario,{}).get("trigger"):fail(f"{scenario} must declare a trigger selector")
 if not isinstance(contract.get("visualInvariants"),list) or len(contract.get("visualInvariants",[]))<8:fail("reference regression contract must define at least eight visual invariants")
 caps=registry.get("capabilities",{});ref=caps.get("canonical-reference-flows-2.1",{});coverage=set(ref.get("coverage",[]));implementations=set(ref.get("implementations",[]))
 if not set(expected).issubset(coverage):fail(f"lifecycle registry reference-flow coverage missing {sorted(set(expected)-coverage)}")
 for path,_ in expected.values():
  if path not in implementations:fail(f"lifecycle registry missing reference implementation {path}")
 expanded=caps.get("expanded-acceptance-matrix-2.1",{});interaction=caps.get("interaction-regression-2.1",{});visual=caps.get("rendered-visual-invariant-regression-2.1",{});pixel=caps.get("visual-regression-2.1",{})
 if expanded.get("status")!="candidate" or expanded.get("implementation")!="contracts/regression/reference-invariants.json":fail("expanded acceptance matrix must be Candidate and point to the regression contract")
 if interaction.get("status")!="candidate" or interaction.get("implementation")!="reference/candidate-2.1-expanded-acceptance.html":fail("interaction regression must be Candidate and point to the expanded rendered harness")
 if visual.get("status")!="candidate" or visual.get("implementation")!="contracts/regression/reference-invariants.json":fail("rendered visual-invariant regression must be Candidate and point to the regression contract")
 if pixel.get("status")!="planned":fail("pixel/screenshot visual regression must remain Planned until baseline artifacts exist")
 for marker in ("scripts/validate_glaze_2_1_regression.py","scripts/validate_glaze_2_1_expanded_rendered.py","reference/candidate-2.1-expanded-acceptance.html"):
  if marker not in workflow:fail(f"2.1 workflow missing expanded regression marker: {marker}")
 if ERRORS:
  print("Glaze UI 2.1 expanded regression validation FAILED",file=sys.stderr)
  for e in ERRORS:print(f"- {e}",file=sys.stderr)
  return 1
 print("Glaze UI 2.1 expanded regression validation passed; Stable remains 2.0.0");print("Pixel screenshot baselines and human Visual Excellence acceptance remain unclaimed.");return 0
if __name__=="__main__":raise SystemExit(main())

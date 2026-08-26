#!/usr/bin/env python3
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DOC = ROOT / "STATES.md"
TOKENS = ROOT / "tokens" / "states.json"
CSS = ROOT / "css" / "glaze.states.css"


def fail(message: str) -> None:
    raise SystemExit(f"state validation failed: {message}")


for path in (DOC, TOKENS, CSS):
    if not path.is_file():
        fail(f"missing {path.relative_to(ROOT)}")

try:
    data = json.loads(TOKENS.read_text())
except Exception as exc:
    fail(f"invalid JSON: {exc}")

if data.get("status") != "1.5-candidate":
    fail("token status must remain 1.5-candidate")
if data.get("stableBaseline") != "1.4.0":
    fail("stable baseline must remain 1.4.0")

expected_states = {
    "default", "hover", "focus-visible", "pressed", "selected", "expanded",
    "disabled", "read-only", "loading", "invalid", "success"
}
if set(data.get("states", [])) != expected_states:
    fail("semantic state set changed")

expected_modalities = {"keyboard", "pointer", "touch", "remote-gamepad", "assistive-technology", "mixed-input"}
if set(data.get("modalities", [])) != expected_modalities:
    fail("input modality set changed")

focus = data.get("focus", {})
if focus.get("minimumRingWidth") != "2px" or focus.get("minimumRingOffset") != "2px":
    fail("focus ring geometry changed")
for key in (
    "mustRemainVisibleOnAllMaterials", "mustSurviveReducedMotion",
    "mustSurviveReducedTransparency", "mustSurviveConstrainedPerformance",
    "globalOutlineSuppressionForbidden"
):
    if focus.get(key) is not True:
        fail(f"focus invariant disabled: {key}")

semantics = data.get("semantics", {})
for key in (
    "hoverCannotBeSolePath", "touchCannotRequireHover", "tvRemoteUsesFocusNotHover",
    "modalityCannotBeInferredSolelyFromViewport", "pressedDistinctFromSelected",
    "selectedDistinctFromExpanded", "disabledDistinctFromReadonly",
    "disabledRequiresSemanticState", "readonlyRequiresSemanticState",
    "loadingRequiresTruthfulBusyState", "determinateProgressMustBeTruthful",
    "invalidRequiresSemanticStateAndExplanation", "statusCannotRelyOnColorAlone"
):
    if semantics.get(key) is not True:
        fail(f"semantic invariant disabled: {key}")

css = CSS.read_text()
for marker in (
    ":focus-visible", "@media (forced-colors: active)",
    "@media (hover: hover) and (pointer: fine)", '[aria-disabled="true"]',
    '[aria-selected="true"]', '[aria-expanded="true"]', '[aria-busy="true"]',
    '[aria-invalid="true"]', "@media (prefers-reduced-motion: reduce)"
):
    if marker not in css:
        fail(f"CSS state primitive missing: {marker}")

# Never allow the common accessibility anti-pattern to become a global rule.
for forbidden in ("*:focus { outline: none", "*:focus-visible { outline: none", "button:focus { outline: none"):
    if forbidden in css:
        fail(f"forbidden global focus suppression: {forbidden}")

doc = DOC.read_text()
for marker in (
    "Glaze UI 1.5 Candidate", "Glaze UI 1.4.0 remains Stable",
    "hover may supplement but never replace", "TV remote/gamepad",
    "Disabled controls must expose native `disabled` or `aria-disabled=\"true\"`",
    "Read-only content must remain legible", "truthful busy semantics",
    "Privacy Shield", "Wardveil Security", "Everkeep", "GoreeCloud Mesh"
):
    if marker not in doc:
        fail(f"documentation invariant missing: {marker}")

print("Glaze UI 1.5 interaction state/input modality Candidate contract: OK")

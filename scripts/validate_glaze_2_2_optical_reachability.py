#!/usr/bin/env python3
"""Static acceptance for the Glaze UI 2.2 Optical Reachability presentation layer.

The accepted Candidate presentation source remains immutable promotion provenance.
This gate verifies that its consolidated layer still spans Foundation, Structure,
Overlay, Signature/Intelligence inherited styling, accessibility fallbacks and
review-evidence wiring, while the canonical lifecycle binds that exact source to
Glaze UI 2.2.0 Stable. Human approval and rendered/pixel continuity remain
separate evidence and cannot be manufactured by this validator.
"""
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CSS = ROOT / "css" / "glaze-2.2.optical-reachability.candidate.css"
REFERENCE = ROOT / "reference" / "candidate-2.2-optical-reachability-acceptance.html"
REVIEW_CAPTURE = ROOT / "scripts" / "capture_glaze_2_2_optical_component_review.py"
LIFECYCLE = ROOT / "registry" / "lifecycle.json"
WORKFLOW = ROOT / ".github" / "workflows" / "glaze-2.2-candidate.yml"
VERSION = ROOT / "VERSION"
APPROVED_SOURCE = "0411b0f6dd877aea30e2c5674e1acde0105fd97b"


def require(text: str, marker: str, label: str) -> None:
    if marker not in text:
        raise SystemExit(f"Glaze UI 2.2 Optical Reachability validation failed: missing {label}: {marker}")


def main() -> None:
    for path in (CSS, REFERENCE, REVIEW_CAPTURE, LIFECYCLE, WORKFLOW, VERSION):
        if not path.is_file():
            raise SystemExit(f"Glaze UI 2.2 Optical Reachability validation failed: missing {path.relative_to(ROOT)}")

    if VERSION.read_text(encoding="utf-8").strip() != "2.2.0":
        raise SystemExit("Glaze UI 2.2 Optical Reachability validation failed: current Stable VERSION must be 2.2.0")

    css = CSS.read_text(encoding="utf-8")
    page = REFERENCE.read_text(encoding="utf-8")
    capture = REVIEW_CAPTURE.read_text(encoding="utf-8")
    workflow = WORKFLOW.read_text(encoding="utf-8")
    lifecycle = json.loads(LIFECYCLE.read_text(encoding="utf-8"))

    # This comment is intentionally retained in the immutable Candidate source;
    # Stable authority comes from VERSION/lifecycle and the versioned wrapper.
    for marker, label in (
        ('Current Stable remains Glaze UI 2.1.0', 'preserved Candidate source boundary'),
        ('--glz22-optical-control-radius', 'optical geometry tokens'),
        ('.glz22-button', 'Foundation button coverage'),
        ('.glz22-field-control', 'Foundation field coverage'),
        ('.glz22-switch-track', 'Foundation switch coverage'),
        ('.glz22-tabs', 'Structure tabs coverage'),
        ('.glz22-sidebar', 'Structure sidebar coverage'),
        ('.glz22-dock', 'Structure dock coverage'),
        ('.glz22-toolbar', 'Structure toolbar coverage'),
        ('.glz22-thick-overlay', 'Overlay glass coverage'),
        ('.glz22-dialog', 'solid modal decision coverage'),
        ('.glz22-toast', 'feedback coverage'),
        ('[data-glz-transparency="reduced"]', 'Reduced Transparency precedence'),
        ('@media(prefers-reduced-transparency:reduce)', 'system Reduced Transparency precedence'),
        ('@media(forced-colors:active)', 'Forced Colors precedence'),
        ('background:Canvas', 'Forced Colors solid fallback'),
        ('backdrop-filter:none', 'no-blur fallback'),
    ):
        require(css, marker, label)

    for marker, label in (
        ('glaze-2.2.structure.candidate.css', 'Structure base import'),
        ('glaze-2.2.optical-reachability.candidate.css', 'Optical Reachability import'),
        ('id="primary"', 'Foundation sample'),
        ('id="tabs"', 'Structure sample'),
        ('id="popover"', 'Overlay sample'),
        ('id="dialog"', 'solid decision sample'),
        ('id="toast"', 'feedback sample'),
        ('dataset.glzTransparency', 'Reduced Transparency exercise'),
        ('forced-colors: active', 'Forced Colors exercise'),
        ('touch-assistance', 'Touch Assistance exercise'),
    ):
        require(page, marker, label)

    for marker, label in (
        ('optical-components-desktop-light', 'desktop component review case'),
        ('optical-components-mobile-dark', 'mobile component review case'),
        ('optical-components-tablet-reduced-transparency', 'Reduced Transparency review case'),
        ('optical-components-mobile-large-text', 'large-text review case'),
        ('optical-components-mobile-touch-assisted', 'Touch Assistance review case'),
        ('optical-components-desktop-deep-dark', 'Deep Dark review case'),
        ('Evidence only; human approval remains required', 'capture-tool human-review boundary'),
    ):
        require(capture, marker, label)

    if lifecycle.get("currentStable") != "2.2.0" or lifecycle.get("activeCandidate") is not None:
        raise SystemExit("Glaze UI 2.2 Optical Reachability validation failed: lifecycle must identify 2.2.0 Stable with no active Candidate")

    capabilities = lifecycle.get("capabilities", {})
    record = capabilities.get("optical-reachability-component-presentation-2.2")
    if not isinstance(record, dict):
        raise SystemExit("Glaze UI 2.2 Optical Reachability validation failed: lifecycle capability missing")
    expected = {
        "status": "stable",
        "since": "2.2.0",
        "implementation": "css/glaze-2.2.optical-reachability.candidate.css",
        "stableEntrypoint": "css/glaze-2.2.0.css",
        "reference": "reference/candidate-2.2-optical-reachability-acceptance.html",
        "validator": "scripts/validate_glaze_2_2_optical_reachability.py",
        "renderedAcceptance": "scripts/validate_glaze_2_2_optical_reachability_rendered.py",
        "reviewCapture": "scripts/capture_glaze_2_2_optical_component_review.py",
        "humanVisualExcellenceAccepted": True,
        "approvedVisualSource": APPROVED_SOURCE,
        "visualBaselineStatus": "human-approved-source-pinned-stable",
        "scope": "bounded-web-component-presentation",
    }
    for key, value in expected.items():
        if record.get(key) != value:
            raise SystemExit(f"Glaze UI 2.2 Optical Reachability validation failed: lifecycle {key} must be {value!r}")
    if record.get("renderedCaseCount") != 15 or record.get("reviewImageCount") != 6:
        raise SystemExit("Glaze UI 2.2 Optical Reachability validation failed: lifecycle evidence counts drifted")

    visual = capabilities.get("bounded-source-pinned-visual-regression-2.2", {})
    if visual.get("status") != "stable" or visual.get("presentationCurrent") is not True or visual.get("humanVisualExcellenceAccepted") is not True:
        raise SystemExit("Glaze UI 2.2 Optical Reachability validation failed: source-pinned visual baseline must be current, Stable and human-approved")
    if visual.get("baselineRevision") != APPROVED_SOURCE:
        raise SystemExit("Glaze UI 2.2 Optical Reachability validation failed: approved visual source revision drifted")

    for marker in (
        'validate_glaze_2_2_optical_reachability.py',
        'validate_glaze_2_2_optical_reachability_rendered.py',
        'capture_glaze_2_2_optical_component_review.py',
        'Validate Glaze UI 2.2 Optical Reachability component presentation',
        'Validate rendered Glaze UI 2.2 Optical Reachability component presentation',
        'Capture exact-head Glaze UI 2.2 Optical Reachability component review set',
        '.artifacts/glaze-2.2-optical-component-review/*.png',
    ):
        require(workflow, marker, 'workflow integration')

    print('Glaze UI 2.2 Optical Reachability static acceptance: PASS')
    print(f'2.2.0 Stable lifecycle is bound to approved source {APPROVED_SOURCE}; rendered/pixel continuity remains separately mandatory.')


if __name__ == '__main__':
    main()

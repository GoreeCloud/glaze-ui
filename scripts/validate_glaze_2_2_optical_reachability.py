#!/usr/bin/env python3
"""Static acceptance for the Glaze UI 2.2 Optical Reachability presentation layer.

This gate verifies that the consolidated Candidate layer spans Foundation,
Structure, Overlay, Signature/Intelligence inherited styling, accessibility
fallbacks, review-evidence wiring, and lifecycle registration. It does not
approve Human Visual Excellence or Stable promotion.
"""
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CSS = ROOT / "css" / "glaze-2.2.optical-reachability.candidate.css"
REFERENCE = ROOT / "reference" / "candidate-2.2-optical-reachability-acceptance.html"
REVIEW_CAPTURE = ROOT / "scripts" / "capture_glaze_2_2_optical_component_review.py"
LIFECYCLE = ROOT / "registry" / "lifecycle.json"
WORKFLOW = ROOT / ".github" / "workflows" / "glaze-2.2-candidate.yml"


def require(text: str, marker: str, label: str) -> None:
    if marker not in text:
        raise SystemExit(f"Glaze UI 2.2 Optical Reachability validation failed: missing {label}: {marker}")


def main() -> None:
    for path in (CSS, REFERENCE, REVIEW_CAPTURE, LIFECYCLE, WORKFLOW):
        if not path.is_file():
            raise SystemExit(f"Glaze UI 2.2 Optical Reachability validation failed: missing {path.relative_to(ROOT)}")

    css = CSS.read_text(encoding="utf-8")
    page = REFERENCE.read_text(encoding="utf-8")
    capture = REVIEW_CAPTURE.read_text(encoding="utf-8")
    workflow = WORKFLOW.read_text(encoding="utf-8")
    lifecycle = json.loads(LIFECYCLE.read_text(encoding="utf-8"))

    for marker, label in (
        ('Current Stable remains Glaze UI 2.1.0', 'Stable boundary'),
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
        ('Evidence only; human approval remains required', 'human-review boundary'),
    ):
        require(capture, marker, label)

    capabilities = lifecycle.get("capabilities", {})
    record = capabilities.get("optical-reachability-component-presentation-2.2")
    if not isinstance(record, dict):
        raise SystemExit("Glaze UI 2.2 Optical Reachability validation failed: lifecycle capability missing")
    expected = {
        "status": "candidate",
        "since": "2.2.0-candidate.1",
        "implementation": "css/glaze-2.2.optical-reachability.candidate.css",
        "reference": "reference/candidate-2.2-optical-reachability-acceptance.html",
        "validator": "scripts/validate_glaze_2_2_optical_reachability.py",
        "renderedAcceptance": "scripts/validate_glaze_2_2_optical_reachability_rendered.py",
        "reviewCapture": "scripts/capture_glaze_2_2_optical_component_review.py",
        "humanVisualExcellenceAccepted": False,
        "visualBaselineStatus": "superseded-pending-human-review",
    }
    for key, value in expected.items():
        if record.get(key) != value:
            raise SystemExit(f"Glaze UI 2.2 Optical Reachability validation failed: lifecycle {key} must be {value!r}")
    if record.get("renderedCaseCount") != 15 or record.get("reviewImageCount") != 6:
        raise SystemExit("Glaze UI 2.2 Optical Reachability validation failed: lifecycle evidence counts drifted")

    old_visual = capabilities.get("bounded-source-pinned-visual-regression-2.2", {})
    if old_visual.get("presentationCurrent") is not False or old_visual.get("humanVisualExcellenceAccepted") is not False:
        raise SystemExit("Glaze UI 2.2 Optical Reachability validation failed: superseded baseline must remain non-current and non-human-approved")

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
    print('Current Stable remains 2.1.0; Candidate review images are evidence only and do not establish Human Visual Excellence.')


if __name__ == '__main__':
    main()

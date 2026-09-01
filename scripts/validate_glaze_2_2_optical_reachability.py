#!/usr/bin/env python3
"""Static acceptance for the Glaze UI 2.2 Optical Reachability presentation layer.

This gate verifies that the consolidated Candidate layer spans Foundation,
Structure, Overlay, Signature/Intelligence inherited styling, and accessibility
fallbacks. It does not approve Human Visual Excellence or Stable promotion.
"""
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CSS = ROOT / "css" / "glaze-2.2.optical-reachability.candidate.css"
REFERENCE = ROOT / "reference" / "candidate-2.2-optical-reachability-acceptance.html"
WORKFLOW = ROOT / ".github" / "workflows" / "glaze-2.2-candidate.yml"


def require(text: str, marker: str, label: str) -> None:
    if marker not in text:
        raise SystemExit(f"Glaze UI 2.2 Optical Reachability validation failed: missing {label}: {marker}")


def main() -> None:
    for path in (CSS, REFERENCE, WORKFLOW):
        if not path.is_file():
            raise SystemExit(f"Glaze UI 2.2 Optical Reachability validation failed: missing {path.relative_to(ROOT)}")

    css = CSS.read_text(encoding="utf-8")
    page = REFERENCE.read_text(encoding="utf-8")
    workflow = WORKFLOW.read_text(encoding="utf-8")

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
        ('data-glz-transparency', 'Reduced Transparency exercise'),
        ('forced-colors: active', 'Forced Colors exercise'),
        ('touch-assistance', 'Touch Assistance exercise'),
    ):
        require(page, marker, label)

    for marker in (
        'validate_glaze_2_2_optical_reachability.py',
        'validate_glaze_2_2_optical_reachability_rendered.py',
        'Validate Glaze UI 2.2 Optical Reachability component presentation',
        'Validate rendered Glaze UI 2.2 Optical Reachability component presentation',
    ):
        require(workflow, marker, 'workflow integration')

    print('Glaze UI 2.2 Optical Reachability static acceptance: PASS')
    print('Current Stable remains 2.1.0; this Candidate presentation layer does not establish Human Visual Excellence.')


if __name__ == '__main__':
    main()

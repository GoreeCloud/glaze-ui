#!/usr/bin/env python3
"""Current GLAZE UI validator with Stable authority and corrective patch gates."""
from validate_css_import_closure import main as validate_css_import_closure
from validate_glaze_v1_1_patch_candidate import main as validate_patch_candidate
from validate_glaze_v1_1_stable import main as validate_stable_authority


def main() -> int:
    stable_status = validate_stable_authority()
    if stable_status:
        return stable_status
    closure_status = validate_css_import_closure()
    if closure_status:
        return closure_status
    return validate_patch_candidate()


if __name__ == "__main__":
    raise SystemExit(main())

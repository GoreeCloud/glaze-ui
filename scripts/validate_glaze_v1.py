#!/usr/bin/env python3
"""Current GLAZE UI product validator with Stable authority and CSS import-closure gates."""
from validate_css_import_closure import main as validate_css_import_closure
from validate_glaze_v1_1_stable import main as validate_stable_authority


def main() -> int:
    stable_status = validate_stable_authority()
    if stable_status:
        return stable_status
    return validate_css_import_closure()


if __name__ == "__main__":
    raise SystemExit(main())

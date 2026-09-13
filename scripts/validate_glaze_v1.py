#!/usr/bin/env python3
"""Validate current GLAZE UI Stable authority plus preserved V1 release history."""

from validate_consumer_summary import main as validate_consumer_summary
from validate_css_import_closure import main as validate_css_import_closure
from validate_glaze_v1_2_stable import main as validate_v1_2_history
from validate_glaze_v1_3_planned import main as validate_v1_3_history
from validate_glaze_v1_4_stable_authority import main as validate_current_stable


def main() -> int:
    # Current authority fails closed first. The V1.4 validator raises on failure
    # and returns None on success.
    validate_current_stable()

    historical_v12 = validate_v1_2_history()
    if historical_v12:
        return historical_v12

    historical_v13 = validate_v1_3_history()
    if historical_v13:
        return historical_v13

    consumer_result = validate_consumer_summary()
    if consumer_result:
        return consumer_result

    return validate_css_import_closure()


if __name__ == "__main__":
    raise SystemExit(main())

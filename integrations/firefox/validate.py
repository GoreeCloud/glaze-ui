#!/usr/bin/env python3
"""Fail-closed source checks for the Firefox Glaze UI integration."""

from __future__ import annotations

import hashlib
import importlib.util
import json
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parent
MANIFEST = ROOT / "theme" / "manifest.json"
USERCHROME = ROOT / "userchrome" / "userChrome.css"
README = ROOT / "README.md"
ACCEPTANCE = ROOT / "ACCEPTANCE.md"
BUILDER = ROOT / "build_theme.py"

REQUIRED_THEME_COLORS = {
    "frame",
    "tab_background_text",
    "tab_text",
    "tab_selected",
    "tab_line",
    "toolbar",
    "toolbar_text",
    "toolbar_field",
    "toolbar_field_text",
    "toolbar_field_border",
    "toolbar_field_focus",
    "toolbar_field_text_focus",
    "toolbar_field_border_focus",
    "toolbar_field_highlight",
    "toolbar_field_highlight_text",
    "popup",
    "popup_text",
    "sidebar",
    "sidebar_text",
    "ntp_background",
    "ntp_text",
}

FORBIDDEN_REMOTE_MARKERS = ("http://", "https://", "@import url", "url(http")


def require(condition: bool, message: str) -> None:
    if not condition:
        raise SystemExit(f"Firefox Glaze validation failed: {message}")


def validate_manifest() -> None:
    data = json.loads(MANIFEST.read_text(encoding="utf-8"))
    require(data.get("manifest_version") == 2, "theme manifest must use Manifest V2")
    require(data.get("version") == "0.2.0", "integration theme version must be 0.2.0")
    require("Glaze UI 1.3" in data.get("description", ""), "theme description must pin Glaze UI 1.3")

    for variant_name in ("theme", "dark_theme"):
        variant = data.get(variant_name)
        require(isinstance(variant, dict), f"missing {variant_name} variant")
        colors = variant.get("colors", {})
        missing = REQUIRED_THEME_COLORS - colors.keys()
        require(not missing, f"{variant_name} missing colors: {sorted(missing)}")
        properties = variant.get("properties", {})
        require(properties.get("content_color_scheme") == "system", f"{variant_name} must preserve system content color preference")

    require(data["theme"]["properties"].get("color_scheme") == "light", "light theme must declare light chrome")
    require(data["dark_theme"]["properties"].get("color_scheme") == "dark", "dark theme must declare dark chrome")

    gecko = data.get("browser_specific_settings", {}).get("gecko", {})
    require(gecko.get("id") == "glaze-ui-firefox@goreecloud.com", "unexpected Firefox theme ID")
    require(bool(gecko.get("strict_min_version")), "Firefox minimum version must be explicit")

    serialized = json.dumps(data).lower()
    require(not any(marker in serialized for marker in FORBIDDEN_REMOTE_MARKERS), "theme must not contain remote dependencies")


def validate_userchrome() -> None:
    css = USERCHROME.read_text(encoding="utf-8")
    lowered = css.lower()
    for marker in FORBIDDEN_REMOTE_MARKERS:
        require(marker not in lowered, f"userChrome must not contain remote dependency marker {marker!r}")

    required_markers = (
        "--gc-functional-glass",
        "--gc-shape-compact",
        "--gc-shape-standard",
        "--gc-shape-expressive",
        "--gc-shape-pressed",
        "prefers-reduced-motion: reduce",
        "prefers-contrast: more",
        "forced-colors: active",
        "backdrop-filter: none",
        "outline: 3px solid var(--gc-focus)",
    )
    for marker in required_markers:
        require(marker in css, f"userChrome missing Glaze/accessibility marker: {marker}")

    require("clear-glass" not in lowered and "clear glass" not in lowered, "Clear Glass must not be implemented in Firefox chrome CSS")


def validate_documentation() -> None:
    text = README.read_text(encoding="utf-8")
    for marker in (
        "Glaze UI 1.3.0",
        "Functional Glass",
        "GoreeCloud Browser",
        "Mozilla Firefox",
        "runtime visual and accessibility acceptance",
        "Deterministic Test Package",
        "Rollback",
    ):
        require(marker.lower() in text.lower(), f"integration README missing required boundary: {marker}")

    acceptance = ACCEPTANCE.read_text(encoding="utf-8")
    for marker in (
        "Firefox Release",
        "Firefox ESR",
        "Pending",
        "theme package SHA-256",
        "userChrome.css",
        "profile-data loss",
    ):
        require(marker.lower() in acceptance.lower(), f"acceptance contract missing marker: {marker}")


def validate_deterministic_package() -> None:
    spec = importlib.util.spec_from_file_location("firefox_theme_builder", BUILDER)
    require(spec is not None and spec.loader is not None, "unable to load Firefox theme builder")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)

    with tempfile.TemporaryDirectory() as first, tempfile.TemporaryDirectory() as second:
        first_package, first_digest = module.build(Path(first))
        second_package, second_digest = module.build(Path(second))
        first_bytes = first_package.read_bytes()
        second_bytes = second_package.read_bytes()
        require(first_bytes == second_bytes, "theme package build is not deterministic")
        digest = hashlib.sha256(first_bytes).hexdigest()
        require(first_digest.read_text(encoding="utf-8").startswith(digest), "first SHA-256 record does not match package")
        require(second_digest.read_text(encoding="utf-8").startswith(digest), "second SHA-256 record does not match package")


def main() -> None:
    for path in (MANIFEST, USERCHROME, README, ACCEPTANCE, BUILDER):
        require(path.is_file(), f"missing required file: {path.relative_to(ROOT.parent.parent)}")
    validate_manifest()
    validate_userchrome()
    validate_documentation()
    validate_deterministic_package()
    print("Firefox Glaze UI integration source validation passed.")


if __name__ == "__main__":
    main()

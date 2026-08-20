#!/usr/bin/env python3
"""Validate the GoreeCloud Glaze UI Firefox integration for ChatGPT."""

from __future__ import annotations

import hashlib
import json
import subprocess
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
EXT = ROOT / "integrations" / "firefox" / "chatgpt"
MANIFEST = EXT / "manifest.json"
BUILD = EXT / "build_extension.py"
COLLECT = EXT / "collect_acceptance.py"
ACCEPTANCE = EXT / "ACCEPTANCE.md"

ALLOWED_PERMISSIONS = {"storage"}
ALLOWED_HOSTS = {"https://chatgpt.com/*", "https://chat.openai.com/*"}
FORBIDDEN_SOURCE_MARKERS = (
    "<all_urls>",
    "http://*/*",
    "https://*/*",
    "browser.cookies",
    "chrome.cookies",
    "browser.history",
    "chrome.history",
    "browser.webRequest",
    "chrome.webRequest",
    "nativeMessaging",
    "clipboardRead",
    "clipboardWrite",
    "google-analytics",
    "googletagmanager",
)
SOURCE_SUFFIXES = {".js", ".css", ".html", ".json", ".py", ".md"}


def require(condition: bool, message: str) -> None:
    if not condition:
        raise SystemExit(f"validation failed: {message}")


def validate_manifest() -> dict:
    require(MANIFEST.is_file(), "manifest.json is missing")
    manifest = json.loads(MANIFEST.read_text(encoding="utf-8"))
    require(manifest.get("manifest_version") == 3, "manifest_version must be 3")

    permissions = set(manifest.get("permissions", []))
    require(permissions <= ALLOWED_PERMISSIONS, f"unexpected extension permission(s): {sorted(permissions - ALLOWED_PERMISSIONS)}")

    host_permissions = set(manifest.get("host_permissions", []))
    require(host_permissions == ALLOWED_HOSTS, "host permissions must stay ChatGPT-only")
    require(manifest.get("browser_specific_settings", {}).get("gecko", {}).get("id"), "Firefox extension id is required")

    action = manifest.get("action", {})
    require(action.get("default_popup") == "src/popup/popup.html", "toolbar popup must remain the local Glaze control surface")
    return manifest


def validate_local_references(manifest: dict) -> None:
    refs: list[str] = []
    refs.extend(manifest.get("icons", {}).values())

    action = manifest.get("action", {})
    refs.extend(action.get("default_icon", {}).values())
    popup = action.get("default_popup")
    if popup:
        refs.append(popup)

    options = manifest.get("options_ui", {}).get("page")
    if options:
        refs.append(options)

    for script in manifest.get("content_scripts", []):
        refs.extend(script.get("css", []))
        refs.extend(script.get("js", []))
        require(set(script.get("matches", [])) == ALLOWED_HOSTS, "content script scope must stay ChatGPT-only")

    for ref in refs:
        require(not ref.startswith(("http://", "https://", "//")), f"remote resource reference is forbidden: {ref}")
        require((EXT / ref).is_file(), f"referenced extension file does not exist: {ref}")

    popup_html = (EXT / "src/popup/popup.html").read_text(encoding="utf-8")
    require("popup.css" in popup_html and "popup.js" in popup_html, "toolbar popup must load local CSS and JavaScript")


def validate_source_policy() -> None:
    source_files = [
        path for path in EXT.rglob("*")
        if path.is_file() and path.suffix.lower() in SOURCE_SUFFIXES and "dist" not in path.parts
    ]
    require(source_files, "extension contains no source files")

    for path in source_files:
        text = path.read_text(encoding="utf-8")
        for marker in FORBIDDEN_SOURCE_MARKERS:
            require(
                marker not in text,
                f"forbidden broad permission, API, or remote dependency marker {marker!r} in {path.relative_to(ROOT)}",
            )

    readme = (EXT / "README.md").read_text(encoding="utf-8")
    for phrase in (
        "presentation-only",
        "does not intentionally read, store, transmit, export, index, or analyze ChatGPT conversation content",
        "does not intercept authentication material or session tokens",
        "no analytics",
        "deterministic unsigned local-test XPI",
        "ACCEPTANCE.md",
        "collect_acceptance.py",
    ):
        require(phrase.lower() in readme.lower(), f"README privacy/release contract missing phrase: {phrase}")


def validate_acceptance_contract() -> None:
    require(ACCEPTANCE.is_file(), "ACCEPTANCE.md is missing")
    require(COLLECT.is_file(), "collect_acceptance.py is missing")
    text = ACCEPTANCE.read_text(encoding="utf-8").lower()
    for phrase in (
        "source validation and deterministic packaging are prerequisites, not substitutes",
        "built xpi sha-256",
        "keyboard-only navigation",
        "browser zoom/reflow remains usable at 200 percent",
        "no extension-authored network request",
        "does not modify chatgpt authentication or session handling",
        "compatibility / dom-drift review",
        "stable acceptance requires all required scenarios to pass",
        "collect_acceptance.py",
    ):
        require(phrase in text, f"acceptance contract missing phrase: {phrase}")


def validate_deterministic_packaging_and_evidence() -> None:
    require(BUILD.is_file(), "build_extension.py is missing")
    subprocess.run([sys.executable, "-m", "py_compile", str(BUILD), str(COLLECT)], check=True)

    with tempfile.TemporaryDirectory() as first_dir, tempfile.TemporaryDirectory() as second_dir:
        first = Path(first_dir) / "extension.xpi"
        second = Path(second_dir) / "extension.xpi"
        evidence = Path(first_dir) / "acceptance.md"
        subprocess.run([sys.executable, str(BUILD), "--output", str(first)], check=True, stdout=subprocess.PIPE, text=True)
        subprocess.run([sys.executable, str(BUILD), "--output", str(second)], check=True, stdout=subprocess.PIPE, text=True)
        require(first.read_bytes() == second.read_bytes(), "extension packaging is not deterministic")
        digest = hashlib.sha256(first.read_bytes()).hexdigest()
        recorded = first.with_suffix(".xpi.sha256").read_text(encoding="utf-8").split()[0]
        require(recorded == digest, "generated package SHA-256 record does not match package bytes")

        subprocess.run(
            [
                sys.executable,
                str(COLLECT),
                "--xpi", str(first),
                "--revision", "0123456789abcdef0123456789abcdef01234567",
                "--firefox-version", "validation-fixture",
                "--firefox-channel", "release",
                "--output", str(evidence),
            ],
            check=True,
            stdout=subprocess.PIPE,
            text=True,
        )
        evidence_text = evidence.read_text(encoding="utf-8").lower()
        for phrase in (
            "privacy boundary",
            "xpi sha-256",
            "no extension-authored network request",
            "current live chatgpt interface was reviewed for selector/dom drift",
            "pass — all blocking scenarios passed",
            "fail — one or more blocking scenarios failed",
        ):
            require(phrase in evidence_text, f"generated acceptance evidence missing phrase: {phrase}")
        for forbidden in (
            "conversation text:",
            "prompt text:",
            "response text:",
            "cookie value:",
            "session token:",
            "browser history:",
        ):
            require(forbidden not in evidence_text, f"generated acceptance evidence exposes forbidden field: {forbidden}")


def main() -> None:
    manifest = validate_manifest()
    validate_local_references(manifest)
    validate_source_policy()
    validate_acceptance_contract()
    validate_deterministic_packaging_and_evidence()
    print("Firefox ChatGPT Glaze UI extension validation passed.")


if __name__ == "__main__":
    main()

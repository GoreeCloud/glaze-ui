#!/usr/bin/env python3
"""Validate the GoreeCloud Glaze UI Firefox integration for ChatGPT."""

from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
EXT = ROOT / "integrations" / "firefox" / "chatgpt"
MANIFEST = EXT / "manifest.json"

ALLOWED_PERMISSIONS = {"storage"}
ALLOWED_HOSTS = {"https://chatgpt.com/*", "https://chat.openai.com/*"}
FORBIDDEN_RUNTIME_MARKERS = (
    "<all_urls>",
    "http://*/*",
    "https://*/*",
    "browser.cookies",
    "browser.history",
    "browser.webRequest",
    "browser.proxy",
    "browser.downloads",
    "nativeMessaging",
    "clipboardRead",
    "clipboardWrite",
    "google-analytics",
    "googletagmanager",
)


def require(condition: bool, message: str) -> None:
    if not condition:
        raise SystemExit(f"validation failed: {message}")


def validate_manifest() -> dict:
    require(MANIFEST.is_file(), "manifest.json is missing")
    manifest = json.loads(MANIFEST.read_text(encoding="utf-8"))
    require(manifest.get("manifest_version") == 3, "manifest_version must be 3")
    require(set(manifest.get("permissions", [])) <= ALLOWED_PERMISSIONS, "unexpected extension permission")
    require(set(manifest.get("host_permissions", [])) == ALLOWED_HOSTS, "host permissions must stay ChatGPT-only")
    require(manifest.get("browser_specific_settings", {}).get("gecko", {}).get("id"), "Firefox extension id is required")
    return manifest


def validate_local_references(manifest: dict) -> None:
    refs: list[str] = []
    refs.extend(manifest.get("icons", {}).values())
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


def validate_source_policy() -> None:
    runtime_files = [
        path
        for path in EXT.rglob("*")
        if path.is_file() and path.suffix.lower() in {".json", ".js", ".css", ".html", ".svg"}
    ]
    require(runtime_files, "extension contains no runtime source files")
    for path in runtime_files:
        text = path.read_text(encoding="utf-8")
        for token in FORBIDDEN_RUNTIME_MARKERS:
            require(token not in text, f"forbidden broad permission, API, or remote dependency marker {token!r} in {path.relative_to(ROOT)}")

    readme = (EXT / "README.md").read_text(encoding="utf-8")
    for phrase in (
        "presentation-only",
        "does not intentionally read, store, transmit, export, index, or analyze ChatGPT conversation content",
        "does not intercept authentication material or session tokens",
        "no analytics",
    ):
        require(phrase.lower() in readme.lower(), f"README privacy contract missing phrase: {phrase}")


def main() -> None:
    manifest = validate_manifest()
    validate_local_references(manifest)
    validate_source_policy()
    print("Firefox ChatGPT Glaze UI extension validation passed.")


if __name__ == "__main__":
    main()

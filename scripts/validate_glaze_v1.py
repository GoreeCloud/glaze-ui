#!/usr/bin/env python3
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
EXPECTED = "1.0.0"


def fail(message: str) -> None:
    raise SystemExit(f"GLAZE UI V1 validation failed: {message}")


def load_json(path: str):
    with (ROOT / path).open(encoding="utf-8") as f:
        return json.load(f)

if (ROOT / "VERSION").read_text(encoding="utf-8").strip() != EXPECTED:
    fail("VERSION must be 1.0.0")

lifecycle = load_json("registry/lifecycle.json")
if lifecycle.get("officialProductLabel") != "GLAZE UI V1.0":
    fail("lifecycle official product label mismatch")
if lifecycle.get("currentOfficial") != EXPECTED:
    fail("lifecycle currentOfficial mismatch")

catalog = load_json("contracts/components/v1/catalog.json")
if catalog.get("version") != EXPECTED or catalog.get("componentCount") != 32:
    fail("V1 component catalog mismatch")

consumers = load_json("consumers/registry.json")
if consumers.get("requiredConsumerVersion") != EXPECTED:
    fail("consumer target mismatch")

required = [
    "GLAZE_UI_V1_0.md",
    "css/glaze-v1.0.0.css",
    "js/glaze-v1.0.0.mjs",
    "contracts/system-shell/glaze-system-shell-v1.json",
    "acceptance/v1.0-stable.md",
]
for rel in required:
    if not (ROOT / rel).exists():
        fail(f"missing required V1 artifact: {rel}")

# Active filenames must not retain former Glaze UI release namespaces.
# CHANGELOG.md remains because GoreeCloud revision-control policy requires the
# append-oriented audit trail; historical entries do not define current versions.
for path in ROOT.rglob("*"):
    if not path.is_file() or ".git" in path.parts or path.name == "CHANGELOG.md":
        continue
    rel = path.relative_to(ROOT).as_posix().lower()
    forbidden = [
        "glaze-2.2", "glaze_2_2", "glaze-ui-2.2", "glaze_ui_2_2",
        "glaze-2.1", "glaze_2_1", "glaze-ui-2.1", "glaze_ui_2_1",
        "candidate-2.2", "candidate-2.1", "candidate-2.0",
    ]
    if any(marker in rel for marker in forbidden):
        fail(f"former release namespace remains in active filename: {rel}")

print("GLAZE UI V1.0 reset contract: OK")

#!/usr/bin/env python3
"""Validate the GLAZE UI V1.3 Stable ESM graph without executing browser code.

The Stable runtime is browser-targeted, so importing it in plain Node is not a
valid graph check: legitimate modules may reference ``document`` or ``window``
at module initialization. This validator instead resolves the complete local ESM
graph, rejects non-local dependencies, verifies every import stays inside the
repository, and asks Node to syntax-check every discovered module without
executing it.
"""

from __future__ import annotations

from collections import deque
from pathlib import Path
import re
import subprocess

ROOT = Path(__file__).resolve().parents[1]
ENTRYPOINT = ROOT / "js" / "glaze-v1.3.0.mjs"

# Static import/export-from, side-effect import, and literal dynamic import.
SPECIFIER_PATTERNS = (
    re.compile(r"(?:import|export)\s+(?:[^;\n]*?\s+from\s+)?[\"']([^\"']+)[\"']"),
    re.compile(r"import\s*\(\s*[\"']([^\"']+)[\"']\s*\)"),
)


def fail(message: str) -> None:
    raise SystemExit(f"GLAZE UI V1.3 Stable runtime graph validation FAILED: {message}")


def module_specifiers(source: str) -> tuple[str, ...]:
    found: list[str] = []
    for pattern in SPECIFIER_PATTERNS:
        found.extend(pattern.findall(source))
    return tuple(dict.fromkeys(found))


def resolve_local(importer: Path, specifier: str) -> Path:
    if not specifier.startswith(("./", "../")):
        fail(f"Stable runtime module uses non-local dependency {specifier!r} from {importer.relative_to(ROOT)}")

    candidate = (importer.parent / specifier).resolve()
    try:
        candidate.relative_to(ROOT)
    except ValueError:
        fail(f"runtime import escapes repository boundary: {specifier!r} from {importer.relative_to(ROOT)}")

    if candidate.suffix == "":
        candidate = candidate.with_suffix(".mjs")
    if candidate.suffix not in {".mjs", ".js"}:
        fail(f"unsupported runtime module extension for {candidate.relative_to(ROOT)}")
    if not candidate.is_file():
        fail(f"unresolved runtime import {specifier!r} from {importer.relative_to(ROOT)}")
    return candidate


def main() -> None:
    if not ENTRYPOINT.is_file():
        fail("missing Stable runtime entrypoint js/glaze-v1.3.0.mjs")

    queue: deque[Path] = deque([ENTRYPOINT.resolve()])
    visited: set[Path] = set()

    while queue:
        module = queue.popleft()
        if module in visited:
            continue
        visited.add(module)

        try:
            source = module.read_text(encoding="utf-8")
        except UnicodeDecodeError as exc:
            fail(f"runtime module is not valid UTF-8: {module.relative_to(ROOT)}: {exc}")

        for specifier in module_specifiers(source):
            dependency = resolve_local(module, specifier)
            if dependency not in visited:
                queue.append(dependency)

    for module in sorted(visited):
        completed = subprocess.run(
            ["node", "--check", str(module)],
            cwd=ROOT,
            text=True,
            capture_output=True,
            check=False,
        )
        if completed.returncode != 0:
            detail = (completed.stderr or completed.stdout).strip()
            fail(f"syntax check failed for {module.relative_to(ROOT)}: {detail}")

    relative_modules = [str(path.relative_to(ROOT)) for path in sorted(visited)]
    if "js/glaze-v1.3.0.mjs" not in relative_modules:
        fail("Stable runtime entrypoint disappeared from resolved graph")

    print(f"GLAZE UI V1.3 Stable runtime module graph: PASS ({len(relative_modules)} local modules)")
    print("Browser-targeted modules were resolved and syntax-checked without executing DOM-dependent initialization.")


if __name__ == "__main__":
    main()

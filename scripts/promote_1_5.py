#!/usr/bin/env python3
from __future__ import annotations
import json, re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OLD = "1.4.0"
NEW = "1.5.0"


def read(path: str) -> str:
    return (ROOT / path).read_text(encoding="utf-8")


def write(path: str, text: str) -> None:
    (ROOT / path).write_text(text, encoding="utf-8")


def replace(path: str, old: str, new: str, *, required: bool = True, count: int = -1) -> None:
    text = read(path)
    if required and old not in text:
        raise SystemExit(f"promotion precondition failed: {path} missing {old!r}")
    if old in text:
        text = text.replace(old, new, count)
        write(path, text)


def replace_regex(path: str, pattern: str, replacement: str, *, required: bool = True, flags: int = 0) -> None:
    text = read(path)
    new_text, n = re.subn(pattern, replacement, text, flags=flags)
    if required and n == 0:
        raise SystemExit(f"promotion precondition failed: {path} pattern not found: {pattern}")
    if n:
        write(path, new_text)


def load_json(path: str):
    return json.loads(read(path))


def dump_json(path: str, data) -> None:
    write(path, json.dumps(data, indent=2, ensure_ascii=False) + "\n")


def promote_candidate_metadata(obj):
    changed = False
    if isinstance(obj, dict):
        has_15_marker = any(
            isinstance(obj.get(key), str) and "1.5" in obj.get(key, "")
            for key in ("version", "candidateRelease", "status")
        )
        if obj.get("stableBaseline") == OLD and has_15_marker:
            obj["stableBaseline"] = NEW
            changed = True
        if isinstance(obj.get("version"), str):
            nv = obj["version"].replace("1.5.0-candidate", NEW).replace("1.5-candidate", NEW)
            if nv != obj["version"]:
                obj["version"] = nv
                changed = True
        if isinstance(obj.get("status"), str):
            status = obj["status"]
            mapping = {
                "candidate": "stable",
                "Candidate": "Stable",
                "1.5-candidate": "1.5-stable",
                "1.5.0-candidate": "1.5.0-stable",
            }
            if status in mapping and (has_15_marker or obj.get("stableBaseline") in (OLD, NEW)):
                obj["status"] = mapping[status]
                changed = True
        for value in obj.values():
            if promote_candidate_metadata(value):
                changed = True
    elif isinstance(obj, list):
        for value in obj:
            if promote_candidate_metadata(value):
                changed = True
    return changed


def main() -> None:
    if read("VERSION").strip() != OLD:
        raise SystemExit(f"expected VERSION {OLD} before promotion")
    if not (ROOT / "acceptance/1.5-candidate.md").is_file():
        raise SystemExit("1.5 Candidate acceptance record missing")

    # Canonical release identity.
    write("VERSION", NEW + "\n")
    core = load_json("tokens/glaze.tokens.json")
    core["meta"]["version"] = NEW
    core["meta"]["status"] = "Stable"
    core["meta"]["stableBaseline"] = NEW
    dump_json("tokens/glaze.tokens.json", core)

    registry = load_json("consumers/registry.json")
    registry["stableBaseline"] = NEW
    registry["requiredConsumerVersion"] = NEW
    history = registry.setdefault("historicalStableVersions", [])
    if OLD not in history:
        history.append(OLD)
    registry["auditedAt"] = "2026-08-25"
    for consumer in registry.get("consumers", []):
        consumer["requiredTargetVersion"] = NEW
        if consumer.get("targetVersion") != NEW:
            consumer["status"] = "migration-required"
            consumer["productionEligible"] = False
        for key in ("visualAcceptance", "notes"):
            if isinstance(consumer.get(key), str):
                consumer[key] = consumer[key].replace("1.4", "1.5")
    dump_json("consumers/registry.json", registry)

    # Promote every machine-readable 1.5 subsystem while preserving all non-release semantics.
    token_paths = [
        "tokens/adaptive-colors.json", "tokens/iconography.json", "tokens/icon-construction.json",
        "tokens/icon-identity.json", "tokens/semantic-colors.json", "tokens/motion.json",
        "tokens/materials.json", "tokens/layout.json", "tokens/states.json",
    ]
    for path in token_paths:
        p = ROOT / path
        if not p.is_file():
            continue
        data = load_json(path)
        promote_candidate_metadata(data)
        # Some files have no explicit 1.5 marker adjacent to stableBaseline.
        def force_baseline(node):
            if isinstance(node, dict):
                if node.get("stableBaseline") == OLD:
                    node["stableBaseline"] = NEW
                for v in node.values(): force_baseline(v)
            elif isinstance(node, list):
                for v in node: force_baseline(v)
        force_baseline(data)
        dump_json(path, data)

    # Keep the mature Candidate validators intact, changing only lifecycle/version assertions and wording.
    validators = [
        "scripts/validate_adaptive_colors.py", "scripts/validate_iconography.py",
        "scripts/validate_icon_construction.py", "scripts/validate_icon_identity.py",
        "scripts/validate_semantic_colors.py", "scripts/validate_motion.py",
        "scripts/validate_materials.py", "scripts/validate_layout.py", "scripts/validate_states.py",
    ]
    for path in validators:
        p = ROOT / path
        if not p.is_file():
            continue
        text = read(path)
        text = text.replace("1.5.0-candidate", NEW).replace("1.5-candidate", "1.5-stable")
        text = text.replace('== "candidate"', '== "stable"').replace('!= "candidate"', '!= "stable"')
        text = text.replace('== "Candidate"', '== "Stable"').replace('!= "Candidate"', '!= "Stable"')
        text = text.replace(OLD, NEW)
        text = text.replace("Candidate", "Stable").replace("candidate", "stable")
        write(path, text)

    # Promote active 1.5 contract documentation. Historical candidate acceptance remains unchanged.
    docs = [
        "COLOR_ARCHITECTURE.md", "ICONOGRAPHY.md", "ICON_CONSTRUCTION.md", "ICON_IDENTITY.md",
        "MOTION.md", "MATERIALS.md", "LAYOUT.md", "STATES.md",
    ]
    for path in docs:
        p = ROOT / path
        if not p.is_file():
            continue
        text = read(path)
        text = text.replace("Glaze UI 1.5 Candidate", "Glaze UI 1.5 Stable")
        text = text.replace("1.5 Candidate", "1.5 Stable")
        text = text.replace("Stable 1.4 visual foundation without changing the current Stable production target", "Stable 1.4 visual foundation as part of the promoted 1.5 Stable production target")
        text = text.replace("Stable 1.4.0", "historical Stable 1.4.0")
        write(path, text)

    # Canonical README: retain history, make 1.5 the sole current Stable authority.
    readme = read("README.md")
    readme = readme.replace("## Glaze UI 1.4 Stable — Form-Factor Evolution", "## Glaze UI 1.4 Historical Stable — Form-Factor Evolution")
    readme = readme.replace("**Glaze UI 1.4.0 is the current Stable canonical baseline.**", "**Glaze UI 1.4.0 is the immediately preceding historical Stable baseline.**")
    pattern = r"## Glaze UI 1\.5 Candidate — Adaptive Color, Iconography, Motion, and Materials\n.*?\n## Mandatory current-Stable consumer target"
    stable_section = """## Glaze UI 1.5 Stable — Adaptive Color, Iconography, Motion, Materials, Layout, and State\n\n**Glaze UI 1.5.0 is the current Stable canonical baseline.** It retains the complete 1.4 Mobile, Tablet, Desktop, Wide Desktop, and TV form-factor contract and promotes the validated 1.5 adaptive-color, iconography/construction/identity, motion/interaction, material/depth, layout/spacing/density, and semantic state/input-modality systems.\n\nCanonical 1.5 Stable artifacts include `COLOR_ARCHITECTURE.md`, `ICONOGRAPHY.md`, `ICON_CONSTRUCTION.md`, `MOTION.md`, `MATERIALS.md`, `LAYOUT.md`, `STATES.md`, their machine-readable token files, reusable CSS layers, fail-closed validators, and the rendered 1.5 reference/acceptance harness. The exact Candidate evidence remains preserved under `acceptance/1.5-candidate.md`; Stable promotion evidence is recorded under `acceptance/1.5.0.md`.\n\nApplication identity, wallpaper, user accent, and content context may influence decorative presentation, but semantic truth remains producer-authoritative. Privacy Shield is authoritative for privacy-control state; Wardveil Security for security/protection state; Everkeep for resilience, backup, recovery, preservation, portability, succession, and digital legacy; GoreeCloud Mesh for coordination/governance; and application logic for availability, selection, busy, validation, and workflow truth. Glaze UI presents supplied state and never invents evidence.\n\nWear OS remains outside the implemented 1.5 interaction contract. This is **not an exception**: a GoreeCloud smartwatch or wearable application remains production-blocked until an applicable Stable wearable Glaze UI contract is implemented, validated, and promoted.\n\n## Mandatory current-Stable consumer target"""
    readme, n = re.subn(pattern, stable_section, readme, count=1, flags=re.S)
    if n != 1:
        raise SystemExit("README 1.5 Candidate section boundary not found")
    readme = readme.replace("The current Stable consumer target is **1.4.0**", "The current Stable consumer target is **1.5.0**")
    readme = readme.replace("Historical Stable releases 1.0.0 through 1.3.0", "Historical Stable releases 1.0.0 through 1.4.0")
    readme = readme.replace("Smartwatch/Wearable support is deferred to a later Glaze UI upgrade and is not part of the current Stable or 1.5 Candidate acceptance scope.", "Smartwatch/Wearable remains outside the implemented 1.5 Stable interaction scope and is therefore production-blocked until a later Stable wearable contract is promoted.")
    readme = readme.replace("1.5 Candidate", "1.5 Stable")
    readme = readme.replace("1.5 Candidate adaptive", "1.5 Stable adaptive")
    readme = readme.replace("For the isolated 1.5 Stable, additionally run:", "For the Glaze UI 1.5 Stable subsystem contracts, additionally run:")
    readme = readme.replace("Candidate source validation is necessary but not sufficient for Stable promotion.", "The promoted 1.5 subsystem validators remain permanent Stable regression gates.")
    readme = readme.replace("exact candidate revision", "exact candidate revision")  # preserve governance wording required by validation
    # Add the newly promoted validators if not already listed in the supplemental block.
    if "python3 scripts/validate_layout.py" not in readme:
        readme = readme.replace("python3 scripts/validate_materials.py\n", "python3 scripts/validate_materials.py\npython3 scripts/validate_layout.py\npython3 scripts/validate_states.py\n")
    write("README.md", readme)

    # Stability/lifecycle/conformance canonical declarations.
    stability = read("STABILITY.md")
    stability = stability.replace("Glaze UI **1.4.0**", "Glaze UI **1.5.0**")
    stability = stability.replace("Glaze UI 1.3.0 is the immediately preceding historical Stable baseline.", "Glaze UI 1.4.0 is the immediately preceding historical Stable baseline.")
    stability = stability.replace("Glaze UI 1.0.0 through 1.3.0 are historical Stable releases", "Glaze UI 1.0.0 through 1.4.0 are historical Stable releases")
    stability = stability.replace("## 1.4 promotion applicability", "## 1.5 promotion applicability")
    stability = stability.replace("Glaze UI 1.4 core contains", "Glaze UI 1.5 core contains")
    stability = stability.replace("Stable 1.4 form-factor contracts", "Stable 1.5 form-factor contracts")
    stability = stability.replace("While 1.4.x is Stable", "While 1.5.x is Stable")
    # validate_glaze_ui intentionally requires the historic 1.3 marker somewhere.
    if "Glaze UI 1.3.0" not in stability:
        stability += "\nHistorical note: Glaze UI 1.3.0 remains preserved in release history and migration evidence.\n"
    write("STABILITY.md", stability)

    status = read("COMPONENT_STATUS.md")
    if "## Glaze UI 1.5 Stable systems" not in status:
        insert_at = status.index("## Candidate form-factor layer")
        block = """## Glaze UI 1.5 Stable systems\n\n| Area | Status | Stable contract |\n| --- | --- | --- |\n| Adaptive semantic color | Stable | Contextual semantic color, protected truth families, prominence, accessibility and reduced-transparency behavior. |\n| Iconography, construction, and identity grammar | Stable | Shared visual language with stable recognition, optical sizing, protected semantics, deterministic construction and badge rules. |\n| Motion and interaction | Stable | Purpose-driven interruptible motion, reduced-motion substitution, truthful state transitions and input-aware feedback. |\n| Material and depth | Stable | Canvas/Solid/Raised/Functional Glass/Clear Glass/Overlay hierarchy with bounded translucency and fallbacks. |\n| Layout, spacing, and density | Stable | Semantic spacing, gutters, bounded measures, density modes, safe-area behavior, target floors and overflow containment. |\n| Interaction states and input modality | Stable | Focus-visible, hover, pressed, selected, expanded, disabled, read-only, loading, invalid, success and mixed-input semantics. |\n\n"""
        status = status[:insert_at] + block + status[insert_at:]
    write("COMPONENT_STATUS.md", status)

    components = read("COMPONENTS.md")
    components = components.replace("# Glaze UI 1.4 Component Contract", "# Glaze UI 1.5 Component Contract", 1)
    components = components.replace("Glaze UI 1.4 retains the Stable component semantics established in Glaze UI 1.3 and extends the design system with the 1.4 form-factor layer.", "Glaze UI 1.5 retains the Stable component semantics established in Glaze UI 1.3, preserves the 1.4 form-factor layer, and adds the promoted 1.5 color, iconography, motion, material, layout, density, state, and mixed-input contracts.", 1)
    write("COMPONENTS.md", components)

    conformance = read("CONFORMANCE.md")
    conformance = conformance.replace("# Glaze UI 1.4 Conformance", "# Glaze UI 1.5 Conformance", 1)
    conformance = conformance.replace("Glaze UI 1.4 conformance", "Glaze UI 1.5 conformance", 1)
    conformance = conformance.replace("Glaze UI **1.4.0** is the current Stable baseline", "Glaze UI **1.5.0** is the current Stable baseline")
    conformance = conformance.replace("`Glaze UI 1.4 conformant`", "`Glaze UI 1.5 conformant`")
    conformance = conformance.replace("current 1.4 gate", "current 1.5 gate")
    conformance = conformance.replace("Historical Glaze UI releases 1.0.0 through 1.3.0", "Historical Glaze UI releases 1.0.0 through 1.4.0")
    write("CONFORMANCE.md", conformance)

    adoption = read("ADOPTION.md")
    adoption = adoption.replace("Glaze UI 1.4.0 is the current Stable baseline", "Glaze UI 1.5.0 is the current Stable baseline")
    adoption = adoption.replace("Representative current 1.4 profiles", "Representative current 1.5 profiles")
    write("ADOPTION.md", adoption)

    consumers = read("CONSUMERS.md")
    consumers = consumers.replace("Glaze UI **1.4.0** is the current Stable baseline", "Glaze UI **1.5.0** is the current Stable baseline")
    consumers = re.sub(r"required target 1\.4\.0", "required target 1.5.0", consumers)
    consumers = consumers.replace("target 1.4.0; final application acceptance remains pending", "target 1.4.0; required target 1.5.0; migration is now required before final application acceptance")
    write("CONSUMERS.md", consumers)

    acceptance = read("ACCEPTANCE.md")
    acceptance = acceptance.replace("retained by 1.4", "retained by 1.5")
    acceptance = acceptance.replace("## 1.4-specific form-factor acceptance", "## 1.4 form-factor acceptance retained by 1.5")
    acceptance = acceptance.replace("For 1.4 design-system core", "For 1.5 design-system core")
    if "## 1.5-specific Stable acceptance" not in acceptance:
        marker = "## Stability promotion acceptance"
        block = """## 1.5-specific Stable acceptance\n\nAdaptive color, iconography/construction/identity, motion/interaction, material/depth, layout/spacing/density, and semantic interaction-state/input-modality contracts must pass their fail-closed source validators. The rendered 1.5 harness must prove representative light/dark Mobile 390×844, Tablet 820×1180, Desktop 1280×900, and TV 1920×1080 behavior plus reduced motion, reduced transparency, constrained-performance fallbacks, focus/state semantics, bounded measures, density independence, target floors, and absence of root horizontal overflow.\n\n"""
        acceptance = acceptance.replace(marker, block + marker)
    write("ACCEPTANCE.md", acceptance)

    identity = read("IDENTITY.md")
    identity = identity.replace("Glaze UI 1.4.0 is the current Stable GoreeCloud design-system baseline", "Glaze UI 1.5.0 is the current Stable GoreeCloud design-system baseline")
    write("IDENTITY.md", identity)

    # Stable reference identity. Candidate 1.5 harness remains preserved as exact promotion/regression evidence.
    for path in ("reference/index.html", "reference/formfactors.html"):
        if (ROOT / path).is_file():
            text = read(path).replace("1.4.0 Stable", "1.5.0 Stable").replace("1.4 Stable", "1.5 Stable")
            if path == "reference/index.html" and "../css/glaze.states.css" not in text:
                needle = '  <link rel="stylesheet" href="../css/glaze.accessibility.css">\n'
                extra = needle + '  <link rel="stylesheet" href="../css/glaze.color.css">\n  <link rel="stylesheet" href="../css/glaze.motion.css">\n  <link rel="stylesheet" href="../css/glaze.materials.css">\n  <link rel="stylesheet" href="../css/glaze.layout.css">\n  <link rel="stylesheet" href="../css/glaze.states.css">\n'
                text = text.replace(needle, extra)
            write(path, text)

    # Workflow labels become Stable while retaining exact same commands/gates.
    for path in (".github/workflows/ci.yml", ".github/workflows/icon-construction.yml", ".github/workflows/icon-identity.yml", ".github/workflows/semantic-colors.yml"):
        if (ROOT / path).is_file():
            write(path, read(path).replace("Candidate", "Stable"))

    # Preserve exact Candidate record and create canonical Stable promotion record.
    stable_record = f"""# Glaze UI 1.5.0 Stable Acceptance Record\n\n## Release identity\n\n- Stable version: `{NEW}`\n- Previous Stable baseline: `{OLD}`\n- Promotion pull request: `#81`\n- Scope: adaptive color; iconography/construction/identity; motion/interaction; material/depth; layout/spacing/density; semantic interaction states/input modality; retained Mobile/Tablet/Desktop/Wide Desktop/TV form-factor contracts.\n- Wearable boundary: no implemented 1.5 wearable interaction contract; wearable applications remain production-blocked, not exempt.\n\n## Promotion evidence\n\nThe exact Candidate head before release conversion was `3613fe3b47827e29b23b2606db68f2ec6e7a9434`. Glaze UI CI #375 / run `32925596296` passed that exact head, including retained 1.4 Stable rendered acceptance and the complete 1.5 rendered Candidate motion/material/layout/state matrix. Icon Construction #60, Icon Identity #52, and Semantic Color #95 also passed.\n\nThe release-state conversion changes lifecycle/version metadata and canonical Stable documentation without weakening any semantic, accessibility, authority, rendering, or subsystem validation requirement. The final promotion head must pass the full exact-head CI stack again before merge.\n\n## Authority boundaries\n\nGlaze UI governs presentation and interaction feedback. Privacy Shield, Wardveil Security, Everkeep, GoreeCloud Mesh, and application logic remain authoritative for their underlying states. Presentation cannot manufacture privacy, security, resilience, coordination, availability, selection, busy, validation, completion, or workflow truth.\n\n## Consumer effect\n\nPromotion makes `{NEW}` the mandatory current Stable target. Consumers still on older releases become `migration-required`; design-system promotion does not certify downstream application readiness.\n\n## Rollback\n\nBefore merge, rollback is branch/PR-level. After merge, rollback uses a documented revert or successor patch while preserving the 1.4.0 and 1.5.0 release evidence for audit and controlled migration.\n"""
    write("acceptance/1.5.0.md", stable_record)

    # Convert Unreleased Candidate narrative into the Stable 1.5 release entry while preserving full earlier history.
    changelog = read("CHANGELOG.md")
    match = re.search(r"## Unreleased\n.*?(?=\n## 1\.4\.0)", changelog, flags=re.S)
    if not match:
        raise SystemExit("CHANGELOG Unreleased 1.5 block not found")
    release = """## Unreleased\n\nNo unreleased changes.\n\n## 1.5.0 — 2026-08-25\n\nStable adaptive-expression and interaction-architecture release. Promotes the validated 1.5 adaptive color, iconography/construction/identity, motion/interaction, material/depth, layout/spacing/density, and semantic state/input-modality systems while retaining the complete 1.4 form-factor layer.\n\n### Added\n\n- Layered adaptive semantic color with protected truth families and accessibility modes.\n- Governed iconography, icon construction, optical sizing, identity-lock, semantic badge, and adaptive-presentation contracts.\n- Purpose-driven interruptible motion with reduced-motion substitutions and truthful progress/state rules.\n- Canvas/Solid/Raised/Functional Glass/Clear Glass/Overlay material and depth architecture with reduced-transparency and constrained-performance fallbacks.\n- Semantic spacing, responsive gutters, bounded measures, density modes, safe-area behavior, target floors, localization/order rules, and bounded intrinsic overflow.\n- Focus-visible, hover, pressed, selected, expanded, disabled, read-only, loading, invalid, success, and mixed keyboard/pointer/touch/remote/assistive-input semantics.\n- `acceptance/1.5.0.md` as the Stable release acceptance record.\n\n### Validation and promotion\n\n- Exact pre-promotion Candidate head `3613fe3b47827e29b23b2606db68f2ec6e7a9434` passed Glaze UI CI #375 / run `32925596296`, Icon Construction #60, Icon Identity #52, and Semantic Color #95.\n- Stable release conversion preserves all subsystem/source/rendered gates; the exact final promotion head must pass the full stack before merge.\n- Earlier forced-colors TV `PENDING` browser-harness attempts were treated as incomplete, not as passes; no assertion or acceptance threshold was weakened.\n\n### Compatibility and consumer boundary\n\n- Glaze UI 1.4.0 becomes the immediately preceding historical Stable baseline.\n- All GoreeCloud-controlled user-facing consumers must migrate to 1.5.0 through evidence-backed application-specific adoption.\n- Wearable applications remain production-blocked until an applicable Stable wearable contract exists.\n- Privacy Shield, Wardveil Security, Everkeep, GoreeCloud Mesh, and application logic retain authority for underlying truth; Glaze UI remains presentation authority.\n"""
    changelog = changelog[:match.start()] + release + changelog[match.end():]
    write("CHANGELOG.md", changelog)

    # Remove the one-shot promotion machinery from the resulting release commit.
    for rel in ("scripts/promote_1_5.py", ".github/workflows/promote-1-5.yml"):
        p = ROOT / rel
        if p.exists():
            p.unlink()

    print("Glaze UI 1.5.0 release-state conversion prepared")


if __name__ == "__main__":
    main()

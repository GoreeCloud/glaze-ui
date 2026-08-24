#!/usr/bin/env python3
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DOC = ROOT / "WEARABLES.md"
COMPONENTS = ROOT / "WEARABLE_COMPONENTS.md"
TOKENS = ROOT / "tokens" / "wearable.candidate.tokens.json"
CSS = ROOT / "css" / "glaze.wearable.candidate.css"
REFERENCE = ROOT / "reference" / "wearable-candidate.html"
NATIVE_README = ROOT / "reference" / "native" / "README.md"
WEAR_OS = ROOT / "reference" / "native" / "wear-os" / "GlazeWearableReference.kt"
WEAR_OS_ACTIVITY = ROOT / "reference" / "native" / "wear-os" / "MainActivity.kt"
WEAR_OS_SETTINGS = ROOT / "reference" / "native" / "wear-os" / "buildable" / "settings.gradle.kts"
WEAR_OS_ROOT_BUILD = ROOT / "reference" / "native" / "wear-os" / "buildable" / "build.gradle.kts"
WEAR_OS_APP_BUILD = ROOT / "reference" / "native" / "wear-os" / "buildable" / "app" / "build.gradle.kts"
WEAR_OS_MANIFEST = ROOT / "reference" / "native" / "wear-os" / "buildable" / "app" / "src" / "main" / "AndroidManifest.xml"
WATCH_OS = ROOT / "reference" / "native" / "watchos" / "GlazeWearableReference.swift"
EVIDENCE_TEMPLATE = ROOT / "acceptance" / "wearable-native-evidence.template.json"
CI_WORKFLOW = ROOT / ".github" / "workflows" / "ci.yml"

REQUIRED_DOC_PHRASES = [
    "Status: **Development Candidate**",
    "Current Stable remains: **Glaze UI 1.4.0**",
    "not a shrunken phone UI",
    "48 dp Wear OS minimum actionable target baseline",
    "Rotary/crown input is a first-class enhancement",
    "Reduced-transparency/solid fallback",
    "Real-device validation before application production approval",
    "Passing this validator proves repository consistency only",
]

REQUIRED_ACCEPTANCE = [
    "Compact round display",
    "Compact rectangular display",
    "Touch-only task completion",
    "Rotary/crown-enhanced navigation",
    "Large-text accessibility",
    "Reduced-motion behavior",
    "Glanceable system-hosted surfaces",
    "Interruption and task-state restoration",
    "Native platform rendering",
    "Real-device validation",
]

REQUIRED_COMPONENT_PHRASES = [
    "Wearable action",
    "Wearable list item",
    "Wearable status card",
    "Wearable glance surface",
    "Reduced-transparency behavior",
    "real-device validation",
]


def fail(message: str) -> None:
    raise SystemExit(f"wearable candidate validation failed: {message}")


def require_markers(path: Path, markers: tuple[str, ...], label: str) -> None:
    text = path.read_text(encoding="utf-8")
    for marker in markers:
        if marker not in text:
            fail(f"required {label} marker missing from {path.relative_to(ROOT)}: {marker}")


def main() -> None:
    required_paths = (
        DOC, COMPONENTS, TOKENS, CSS, REFERENCE, NATIVE_README, WEAR_OS,
        WEAR_OS_ACTIVITY, WEAR_OS_SETTINGS, WEAR_OS_ROOT_BUILD, WEAR_OS_APP_BUILD,
        WEAR_OS_MANIFEST, WATCH_OS, EVIDENCE_TEMPLATE, CI_WORKFLOW,
    )
    for path in required_paths:
        if not path.is_file():
            fail(f"required candidate asset is missing: {path.relative_to(ROOT)}")

    text = DOC.read_text(encoding="utf-8")
    for phrase in REQUIRED_DOC_PHRASES + REQUIRED_ACCEPTANCE:
        if phrase not in text:
            fail(f"required contract phrase missing: {phrase}")

    component_text = COMPONENTS.read_text(encoding="utf-8")
    for phrase in REQUIRED_COMPONENT_PHRASES:
        if phrase not in component_text:
            fail(f"required component mapping missing: {phrase}")

    data = json.loads(TOKENS.read_text(encoding="utf-8"))
    candidate = data.get("glaze", {}).get("wearableCandidate", {})
    if candidate.get("status", {}).get("$value") != "development-candidate":
        fail("token lifecycle status must remain development-candidate")

    minimum = candidate.get("target", {}).get("minimumWearOs", {}).get("$value", {})
    if minimum != {"value": 48, "unit": "dp"}:
        fail("Wear OS minimum target must remain 48 dp in this candidate")

    resilience = candidate.get("resilience", {})
    for key in ("reducedMotion", "reducedTransparency", "solidFallback", "largeText"):
        if resilience.get(key, {}).get("$value") is not True:
            fail(f"required resilience token is not enabled: {key}")

    stable_tokens = json.loads((ROOT / "tokens" / "glaze.tokens.json").read_text(encoding="utf-8"))
    if "wearableCandidate" in stable_tokens.get("glaze", {}):
        fail("candidate wearable tokens must not be injected into Stable glaze.tokens.json")

    require_markers(CSS, (
        'data-glaze-wearable-candidate',
        'prefers-reduced-motion',
        'forced-colors',
        '--glaze-wearable-target: 48px',
    ), "candidate CSS")

    require_markers(REFERENCE, (
        'data-glaze-watch-shape="round"',
        'data-glaze-watch-shape="rectangular"',
        'Development Candidate only',
        'does not constitute native-platform or real-device acceptance',
    ), "browser reference evidence")

    require_markers(NATIVE_README, (
        'Development Candidate implementation evidence',
        'AGP 9.3.0',
        'Compose BOM 2026.08.00',
        'Wear Compose Material 3 1.5.0',
        'watchOS reference remains source-only',
        'real-device validation',
    ), "native evidence boundary")

    require_markers(WEAR_OS, (
        'TransformingLazyColumn',
        'minimumInteractiveComponentSize',
        'implementation evidence only',
        'rotary behavior',
    ), "Wear OS reference")

    require_markers(WEAR_OS_ACTIVITY, (
        'class MainActivity : ComponentActivity()',
        'GlazeWearableReference()',
        'compilation proves current-SDK source compatibility only',
    ), "Wear OS activity")

    require_markers(WEAR_OS_ROOT_BUILD, (
        'com.android.application',
        '9.3.0',
        'org.jetbrains.kotlin.plugin.compose',
        '2.3.21',
    ), "Wear OS root build")

    require_markers(WEAR_OS_APP_BUILD, (
        'compileSdk = 37',
        'targetSdk = 36',
        'androidx.compose:compose-bom:2026.08.00',
        'androidx.wear.compose:compose-material3:1.5.0',
        'sourceSets["main"].kotlin.srcDir("../..")',
    ), "Wear OS app build")

    require_markers(WEAR_OS_MANIFEST, (
        'android.hardware.type.watch',
        'android:allowBackup="false"',
        'android:name=".MainActivity"',
    ), "Wear OS manifest")

    require_markers(WATCH_OS, (
        'ScrollView',
        'accessibilityLabel',
        'accessibilityValue',
        'implementation evidence only',
        'Digital Crown',
    ), "watchOS reference")

    require_markers(CI_WORKFLOW, (
        'wear-os-build:',
        'persist-credentials: false',
        'platforms;android-37',
        'gradle-9.5.0-bin.zip',
        '553c78f50dafcd54d65b9a444649057857469edf836431389695608536d6b746',
        'gradle :app:assembleDebug --no-daemon --stacktrace',
    ), "Wear OS CI build")

    evidence = json.loads(EVIDENCE_TEMPLATE.read_text(encoding="utf-8"))
    if evidence.get("status") != "template-only":
        fail("wearable evidence template must remain template-only")
    if evidence.get("glazeUiStableBaseline") != "1.4.0":
        fail("wearable evidence template must identify 1.4.0 as the current Stable baseline")
    if evidence.get("promotion", {}).get("stableEligible") is not False:
        fail("wearable evidence template must fail closed with stableEligible=false")
    for target in ("wearOs", "watchOs"):
        record = evidence.get("targets", {}).get(target, {})
        if record.get("buildResult") != "pending" or record.get("realDevice") != "pending":
            fail(f"{target} template evidence must remain pending until actual acceptance is recorded")

    if 'glaze.wearable.candidate.css' in (ROOT / 'css' / 'glaze.css').read_text(encoding='utf-8'):
        fail("candidate wearable CSS must not be imported by Stable glaze.css")

    print("Glaze UI wearable Development Candidate contract, mappings, browser/native references, build harness, CI build contract, and acceptance template validated.")


if __name__ == "__main__":
    main()

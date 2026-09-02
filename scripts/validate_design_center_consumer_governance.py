#!/usr/bin/env python3
"""Validate that the public Design Center renders and filters canonical consumer governance without semantic drift."""
from __future__ import annotations

import html
import json
import re
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
REGISTRY = ROOT / "consumers" / "registry.json"
SOURCE = ROOT / "website" / "index.html"
SITE_JS = ROOT / "website" / "site.js"
DIST = ROOT / "website" / "dist" / "index.html"
GOVERNANCE_CSS = ROOT / "website" / "dist" / "assets" / "governance.css"
DIST_JS = ROOT / "website" / "dist" / "assets" / "site.js"
TOKEN = "<!-- GLAZE_CONSUMER_GOVERNANCE -->"
CARD = re.compile(
    r'<article class="consumer-card glaze-surface" data-consumer-name="(?P<name>[^"]+)" '
    r'data-consumer-repository="(?P<repository>[^"]+)" data-consumer-status="(?P<status>[^"]+)" '
    r'data-production-eligible="(?P<eligible>true|false)">(?P<body>.*?)</article>',
    re.DOTALL,
)


def req(condition: bool, message: str) -> None:
    if not condition:
        raise SystemExit(f"Design Center consumer governance validation failed: {message}")


def main() -> int:
    data = json.loads(REGISTRY.read_text(encoding="utf-8"))
    stable = str(data.get("stableBaseline", ""))
    audited = str(data.get("auditedAt", ""))
    schema = data.get("schemaVersion")
    consumers = data.get("consumers", [])
    req(stable == "2.2.0", "public governance expects current Stable 2.2.0")
    req(isinstance(schema, int) and schema >= 5, "registry schema must carry source-verifiable consumer evidence")
    req(isinstance(consumers, list) and consumers, "consumer registry is empty")
    req(SOURCE.read_text(encoding="utf-8").count(TOKEN) == 1, "source page must contain exactly one build token")

    subprocess.run(["node", "--check", str(SITE_JS)], cwd=ROOT, check=True)
    subprocess.run([sys.executable, str(ROOT / "website" / "build.py")], cwd=ROOT, check=True)
    req(DIST.is_file() and GOVERNANCE_CSS.is_file() and DIST_JS.is_file(), "governance build artifacts are missing")
    rendered = DIST.read_text(encoding="utf-8")
    css = GOVERNANCE_CSS.read_text(encoding="utf-8")
    js = DIST_JS.read_text(encoding="utf-8")

    req(TOKEN not in rendered, "build token leaked into public artifact")
    for marker in (
        '<section id="governance"',
        f'data-consumer-registry-schema="{schema}"',
        f'data-stable-baseline="{html.escape(stable, quote=True)}"',
        f'data-audited-at="{html.escape(audited, quote=True)}"',
        "Consumer conformance is a state, not a declaration.",
        "Adoption Candidate means current-Stable implementation evidence exists, but it is not production acceptance.",
        "No application is promoted by this page.",
        "Search and status filters only change which registry-backed cards are visible; they never change consumer state or evidence.",
        "Pending-acceptance disclosures copy registry requirements and notes for inspection; opening or reading them does not satisfy those requirements.",
        '<summary>Pending acceptance and notes</summary>',
        "/assets/governance.css",
        'href="#governance">Governance</a>',
        'data-governance-search',
        'data-governance-result role="status" aria-live="polite"',
        'data-governance-consumers',
        'data-governance-status="all" aria-pressed="true"',
    ):
        req(marker in rendered, f"public governance marker missing: {marker}")

    filter_labels = {
        "all": "All",
        "aligned-current-stable": "Aligned current Stable",
        "adoption-candidate": "Adoption Candidate",
        "migration-required": "Migration Required",
        "unverified": "Unverified",
    }
    for status, label in filter_labels.items():
        req(
            f'data-governance-status="{status}"' in rendered and f'>{html.escape(label)}</button>' in rendered,
            f"governance filter missing status option: {status}",
        )

    cards = list(CARD.finditer(rendered))
    req(len(cards) == len(consumers), "rendered consumer-card count differs from registry")
    req(rendered.count('<details class="consumer-acceptance">') == len(consumers), "pending-acceptance disclosure count differs from registry")
    rendered_by_name: dict[str, re.Match[str]] = {}
    for card in cards:
        name = html.unescape(card.group("name"))
        req(name not in rendered_by_name, f"duplicate rendered consumer: {name}")
        rendered_by_name[name] = card

    registered_names = {str(consumer.get("name")) for consumer in consumers if isinstance(consumer, dict)}
    req(set(rendered_by_name) == registered_names, "rendered consumer set differs from canonical registry")

    status_counts: dict[str, int] = {}
    production_count = 0
    for consumer in consumers:
        req(isinstance(consumer, dict), "consumer registry contains a non-object entry")
        name = str(consumer.get("name"))
        repository = str(consumer.get("repository"))
        status = str(consumer.get("status"))
        eligible = consumer.get("productionEligible") is True
        acceptance = str(consumer.get("visualAcceptance", "")).strip()
        notes = str(consumer.get("notes", "")).strip()
        req(bool(acceptance), f"{name} registry acceptance requirements are missing")
        req(bool(notes), f"{name} registry notes are missing")
        card = rendered_by_name[name]
        body = card.group("body")
        req(html.unescape(card.group("repository")) == repository, f"{name} rendered repository differs from registry")
        req(card.group("status") == status, f"{name} rendered status differs from registry")
        req(card.group("eligible") == str(eligible).lower(), f"{name} rendered production eligibility differs from registry")
        status_counts[status] = status_counts.get(status, 0) + 1
        production_count += int(eligible)

        expected_values = [
            repository,
            str(consumer.get("targetVersion")) if consumer.get("targetVersion") else "Not verified",
            str(consumer.get("requiredTargetVersion") or stable),
            "Yes" if eligible else "No",
            acceptance,
            notes,
        ]
        for key in ("referenceRevision", "evidence", "automatedContractPath"):
            value = consumer.get(key)
            if value:
                expected_values.append(str(value))
        if not consumer.get("evidence"):
            expected_values.append(f"Fresh repository-local Glaze UI {stable} evidence required")
        for value in expected_values:
            req(html.escape(value) in body, f"{name} card missing registry-backed value: {value}")
        for label in ("Acceptance requirements", "Registry notes"):
            req(f'<h4>{label}</h4>' in body, f"{name} disclosure missing label: {label}")

    req(f'<span>Audited consumers</span><strong>{len(consumers)}</strong>' in rendered, "consumer summary total drift")
    req(f'<span>Adoption candidates</span><strong>{status_counts.get("adoption-candidate", 0)}</strong>' in rendered, "Adoption Candidate summary drift")
    req(f'<span>Aligned current Stable</span><strong>{status_counts.get("aligned-current-stable", 0)}</strong>' in rendered, "aligned-current-Stable summary drift")
    req(f'<span>Production eligible</span><strong>{production_count}</strong>' in rendered, "production-eligible summary drift")
    req(f'{len(consumers)} of {len(consumers)} consumers shown.' in rendered, "initial visible-result count drift")

    by_repo = {str(consumer.get("repository")): consumer for consumer in consumers if isinstance(consumer, dict)}
    launcher = by_repo.get("GoreeCloud/goreecloud-launcher")
    keyboard = by_repo.get("GoreeCloud/goreecloud-keyboard")
    req(launcher is not None and launcher.get("status") == "migration-required" and launcher.get("targetVersion") == "2.1.0", "Launcher must remain historical 2.1 migration evidence until fresh 2.2 evidence exists")
    req(keyboard is not None and keyboard.get("status") == "adoption-candidate" and keyboard.get("targetVersion") == stable, "Keyboard must remain the verified 2.2 Adoption Candidate")
    req(keyboard.get("automatedContractPath") == "scripts/check_glaze_motion_evaluation.py", "Keyboard source-verification contract drift")

    for marker in (
        "data-governance-search",
        "data-governance-status",
        "data-consumer-repository",
        "card.dataset.consumerStatus===status",
        "card.dataset.consumerRepository",
        "card.hidden=!show",
        "button.setAttribute('aria-pressed'",
        "consumers shown.",
    ):
        req(marker in js, f"governance filtering interaction contract missing: {marker}")

    for marker in (
        ".governance-controls",
        ".governance-search input{width:100%;min-height:48px",
        ".governance-filter-actions button{min-height:48px",
        ".governance-filter-actions button[aria-pressed=\"true\"]",
        ".consumer-card[hidden]{display:none!important}",
        ".consumer-acceptance{",
        ".consumer-acceptance summary{min-height:48px",
        ".consumer-acceptance summary:focus-visible",
        ".consumer-acceptance-body>div{",
        ".governance-summary",
        ".consumer-grid",
        ".consumer-card",
        '@media(max-width:820px)',
        '@media(max-width:640px)',
        '@media(forced-colors:active)',
        'word-break:break-word',
    ):
        req(marker in css, f"governance presentation contract missing: {marker}")

    print(
        "Design Center consumer governance validated: canonical registry schema, exact consumer states and repositories, "
        "source-evidence fields, registry-backed pending-acceptance disclosures, visibility-only search/status filtering, "
        "production boundary, responsive composition, 48px interactive targets, and forced-colors fallback are synchronized."
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

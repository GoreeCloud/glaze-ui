#!/usr/bin/env python3
"""Fail closed when Glaze UI release-state or mandatory consumer records drift from VERSION."""
from __future__ import annotations
import json,re
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
VERSION=(ROOT/'VERSION').read_text(encoding='utf-8').strip()
def require(condition: bool, message: str) -> None:
    if not condition: raise SystemExit(f'Glaze UI release-state validation failed: {message}')
def text(path: str) -> str: return (ROOT/path).read_text(encoding='utf-8')
def main() -> None:
    require(re.fullmatch(r'\d+\.\d+\.\d+',VERSION) is not None,'VERSION must use semantic versioning')
    tokens=json.loads(text('tokens/glaze.tokens.json')); require(tokens['meta']['version']==VERSION,'token metadata does not match VERSION')
    registry=json.loads(text('consumers/registry.json'))
    require(registry.get('schemaVersion')==3,'consumer registry schema must be 3')
    require(registry.get('stableBaseline')==VERSION,'consumer registry Stable baseline differs from VERSION')
    require(registry.get('requiredConsumerVersion')==VERSION,'consumer registry required target differs from VERSION')
    enforcement=registry.get('enforcement',{})
    require(enforcement.get('currentStableRequired') is True,'consumer registry must require current Stable')
    require(enforcement.get('productionExceptionsAllowed') is False,'consumer registry must prohibit production exceptions')
    require('smartwatch' in enforcement.get('platformScope',[]),'consumer registry must cover smartwatch/wearable applications')

    readme=text('README.md'); stability=text('STABILITY.md'); security=text('SECURITY.md'); identity=text('IDENTITY.md'); component_status=text('COMPONENT_STATUS.md'); component_contract=text('COMPONENTS.md'); conformance=text('CONFORMANCE.md'); acceptance=text('ACCEPTANCE.md'); contributing=text('CONTRIBUTING.md'); changelog=text('CHANGELOG.md'); adoption=text('ADOPTION.md'); consumers=text('CONSUMERS.md')
    stable_family=VERSION.rsplit('.',1)[0]

    require(f'Glaze UI {VERSION} is the current Stable canonical baseline' in readme,'README current-Stable declaration is missing or stale')
    require(f'**Stable baseline:** Glaze UI **{VERSION}**' in stability,'STABILITY.md Stable baseline is missing or stale')
    require(f'Glaze UI {stable_family} Stable' in component_status,'COMPONENT_STATUS.md current Stable release family is missing')
    require(component_contract.startswith(f'# Glaze UI {stable_family} Component Contract\n'),'COMPONENTS.md heading does not match the current Stable release family')
    require(f'Glaze UI {stable_family} retains the Stable component semantics established in Glaze UI 1.3' in component_contract,'COMPONENTS.md does not preserve the 1.3-to-current component compatibility boundary')
    require(VERSION in changelog,'CHANGELOG.md does not mention the current VERSION')

    current_stable_pattern=re.compile(r'current Stable(?: canonical)? baseline[^\n]*?Glaze UI\s+(\d+\.\d+\.\d+)',re.IGNORECASE)
    for path in ('README.md','STABILITY.md','COMPONENT_STATUS.md','CONFORMANCE.md','ADOPTION.md','ACCEPTANCE.md'):
        body=text(path)
        for match in current_stable_pattern.finditer(body): require(match.group(1)==VERSION,f'{path} declares stale current Stable version {match.group(1)}')

    stable_surface_hierarchy='Canvas/Solid/Raised/Functional Glass/Clear Glass/Overlay hierarchy'
    require(stable_surface_hierarchy in acceptance,'ACCEPTANCE.md does not use the current Stable material hierarchy')
    require('Canvas, Solid, Raised, Functional Glass, Clear Glass, and Overlay' in conformance,'CONFORMANCE.md does not use the current Stable material hierarchy')
    require('Canvas/Solid/Raised/Glaze/Overlay hierarchy' not in acceptance,'ACCEPTANCE.md still contains the superseded generic Glaze material hierarchy')

    require('## Current-Stable conformance claims' in conformance,'CONFORMANCE.md current-Stable conformance section is missing')
    require(f'Glaze UI **{VERSION}** is the current Stable baseline' in conformance,'CONFORMANCE.md current Stable baseline is missing or stale')
    require('the only active version eligible' in conformance,'CONFORMANCE.md must prohibit superseded active conformance targets')
    require('No documented exception can waive the current-Stable application requirement' in conformance,'CONFORMANCE.md no-exception rule is missing')
    require('Smartwatch/Wearable' in conformance,'CONFORMANCE.md smartwatch/wearable gate is missing')

    require('## Mandatory current-Stable consumer target' in readme,'README mandatory current-Stable consumer section is missing')
    require('the only Glaze UI version that may satisfy current GoreeCloud application conformance' in readme,'README current-Stable exclusivity is missing')
    require('Existing consumers are never grandfathered' in readme,'README no-grandfathering rule is missing')
    require('There are no application-level production exceptions' in readme,'README no-exception rule is missing')
    require('Smartwatch/Wearable' in readme,'README smartwatch/wearable scope is missing')

    require('controlled migration is mandatory rather than optional' in stability,'STABILITY.md mandatory migration boundary is missing')
    require('Applications may not remain on older Stable Glaze UI versions as a conforming production state' in stability,'STABILITY.md superseded-version production block is missing')
    require('Missing Stable platform coverage is not an exception' in stability,'STABILITY.md platform gap must fail closed')
    require('No active 1.4 form-factor capability remains Candidate' in component_status,'1.4 lifecycle reconciliation is incomplete')

    require('current Stable Glaze UI baseline' in security,'SECURITY.md must bind fixes to the current Stable baseline')
    require('the only supported active application target' in security,'SECURITY.md must bind application support to current Stable')
    require('never makes a historical release a supported production target' in security,'SECURITY.md historical maintenance boundary is missing')

    require(f'Glaze UI {VERSION} is the current Stable GoreeCloud design-system baseline' in identity,'IDENTITY.md current-Stable declaration is missing or stale')
    require('Status: **Pending approved canonical artwork**' in identity,'IDENTITY.md must preserve the unresolved artwork status')
    require('No icon, logo, favicon, or product mark is approved as canonical Glaze UI artwork at this time' in identity,'IDENTITY.md must preserve the no-canonical-artwork boundary')
    require('Glaze UI 1.3.0 is the stable GoreeCloud design system' not in identity,'IDENTITY.md still advertises the superseded 1.3 Stable baseline')

    require('## Mandatory current Stable target' in consumers,'CONSUMERS.md mandatory current Stable section is missing')
    require('Migration Required' in consumers,'CONSUMERS.md migration-required state is missing')
    require('smartwatch and wearable applications' in consumers.lower(),'CONSUMERS.md smartwatch scope is missing')
    require('Existing consumers on older releases are migration-required' in adoption,'ADOPTION.md mandatory migration rule is missing')
    require('### Smartwatch and wearables' in adoption,'ADOPTION.md smartwatch/wearable adoption rule is missing')

    required_stable_commands=('python3 scripts/validate_glaze_ui.py','python3 scripts/validate_release_state.py','python3 scripts/validate_form_factors.py','python3 scripts/validate_typography_contract.py','python3 scripts/validate_consumer_registry.py','python3 integrations/firefox/validate.py','python3 website/validate.py','python3 scripts/validate_rendered_reference.py')
    for command in required_stable_commands:
        require(command in readme,f'README.md omits Stable validation command: {command}')
        require(command in contributing,f'CONTRIBUTING.md omits Stable validation command: {command}')
    require('exact candidate revision' in readme,'README.md must preserve exact-candidate validation guidance')
    for profile in ('Mobile — 390 × 844','Tablet — 820 × 1180','Desktop — 1280 × 900','Wide Desktop — 1600 × 1000','TV — 1920 × 1080'):
        require(profile in contributing,f'CONTRIBUTING.md omits Stable acceptance profile: {profile}')
    require('exact PR head' in contributing,'CONTRIBUTING.md must preserve exact-head validation guidance')
    print(f'Glaze UI release-state validation passed for {VERSION}; current-Stable consumer enforcement active')
if __name__=='__main__': main()

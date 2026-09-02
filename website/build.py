#!/usr/bin/env python3
from pathlib import Path
import html
import json
import shutil

ROOT=Path(__file__).resolve().parents[1]
SOURCE=ROOT/'website'; DIST=SOURCE/'dist'; IDENTITY=ROOT/'assets/identity/official/facet'; REGISTRY=ROOT/'consumers/registry.json'
GOVERNANCE_TOKEN='<!-- GLAZE_CONSUMER_GOVERNANCE -->'


def render_consumer_governance(data: dict) -> str:
    stable=str(data.get('stableBaseline',''))
    audited=str(data.get('auditedAt',''))
    schema=data.get('schemaVersion')
    consumers=data.get('consumers',[])
    if not stable or not audited or not isinstance(schema,int) or not isinstance(consumers,list):
        raise SystemExit('consumer registry is missing Design Center governance fields')

    labels={
        'aligned-current-stable':'Aligned — current Stable',
        'adoption-candidate':'Adoption Candidate',
        'migration-required':'Migration Required',
        'unverified':'Unverified',
    }
    counts={status:0 for status in labels}
    production_eligible=0
    cards=[]
    for consumer in consumers:
        if not isinstance(consumer,dict):
            raise SystemExit('consumer registry contains a non-object entry')
        name=str(consumer.get('name',''))
        status=str(consumer.get('status',''))
        if not name or status not in labels:
            raise SystemExit(f'consumer registry contains unsupported Design Center state: {name or "unnamed"} / {status}')
        counts[status]+=1
        eligible=consumer.get('productionEligible') is True
        production_eligible+=int(eligible)
        target=consumer.get('targetVersion')
        required=consumer.get('requiredTargetVersion')
        revision=consumer.get('referenceRevision')
        evidence=consumer.get('evidence')
        contract=consumer.get('automatedContractPath')

        details=[
            ('Recorded target', str(target) if target else 'Not verified'),
            ('Required target', str(required) if required else stable),
            ('Production eligible', 'Yes' if eligible else 'No'),
        ]
        if revision:
            details.append(('Exact revision', str(revision)))
        if evidence:
            details.append(('Evidence', str(evidence)))
        if contract:
            details.append(('Automated contract', str(contract)))
        if not evidence:
            details.append(('Evidence', f'Fresh repository-local Glaze UI {stable} evidence required'))

        detail_html=''.join(
            f'<div><dt>{html.escape(label)}</dt><dd><code>{html.escape(value)}</code></dd></div>'
            for label,value in details
        )
        cards.append(
            f'<article class="consumer-card glaze-surface" data-consumer-name="{html.escape(name,quote=True)}" '
            f'data-consumer-status="{html.escape(status,quote=True)}" data-production-eligible="{str(eligible).lower()}">'
            f'<div class="consumer-card-heading"><h3>{html.escape(name)}</h3>'
            f'<span class="consumer-status" data-status="{html.escape(status,quote=True)}">{html.escape(labels[status])}</span></div>'
            f'<dl>{detail_html}</dl></article>'
        )

    summary=(
        f'<div class="governance-summary" role="list" aria-label="Glaze UI consumer governance summary">'
        f'<article role="listitem"><span>Stable baseline</span><strong>{html.escape(stable)}</strong></article>'
        f'<article role="listitem"><span>Audited consumers</span><strong>{len(consumers)}</strong></article>'
        f'<article role="listitem"><span>Adoption candidates</span><strong>{counts["adoption-candidate"]}</strong></article>'
        f'<article role="listitem"><span>Aligned current Stable</span><strong>{counts["aligned-current-stable"]}</strong></article>'
        f'<article role="listitem"><span>Production eligible</span><strong>{production_eligible}</strong></article>'
        f'</div>'
    )
    return (
        f'<section id="governance" class="section-block consumer-governance" data-consumer-registry-schema="{schema}" '
        f'data-stable-baseline="{html.escape(stable,quote=True)}" data-audited-at="{html.escape(audited,quote=True)}">'
        f'<div class="section-heading"><span class="eyebrow">Evidence-backed adoption</span>'
        f'<h2>Consumer conformance is a state, not a declaration.</h2>'
        f'<p>The Design Center renders this inspection surface from the canonical consumer registry at build time. '
        f'Adoption Candidate means current-Stable implementation evidence exists, but it is not production acceptance. '
        f'Migration Required and Unverified remain production-blocking on the Glaze UI gate.</p></div>'
        f'{summary}'
        f'<p class="governance-boundary glaze-surface-raised"><strong>Acceptance boundary:</strong> '
        f'No application is promoted by this page. Product-specific rendered/native, accessibility, supported-platform and representative-device acceptance remain authoritative.</p>'
        f'<div class="consumer-grid">{"".join(cards)}</div>'
        f'<p class="registry-provenance">Registry schema {schema} · audited {html.escape(audited)} · current Stable {html.escape(stable)}.</p>'
        f'</section>'
    )


if DIST.exists(): shutil.rmtree(DIST)
(DIST/'assets').mkdir(parents=True)
index=(SOURCE/'index.html').read_text(encoding='utf-8')
if index.count(GOVERNANCE_TOKEN)!=1:
    raise SystemExit('Design Center source must contain exactly one consumer-governance build token')
registry=json.loads(REGISTRY.read_text(encoding='utf-8'))
(DIST/'index.html').write_text(index.replace(GOVERNANCE_TOKEN,render_consumer_governance(registry)),encoding='utf-8')
for name in ('404.html','_headers'): shutil.copy2(SOURCE/name,DIST/name)
for name in ('site.css','governance.css','identity.css','site.js'): shutil.copy2(SOURCE/name,DIST/'assets'/name)
for name in (
    'glaze.css','glaze.controls.css','glaze.expressive.css','glaze.formfactors.css','glaze.accessibility.css',
    'glaze.color.css','glaze.motion.css','glaze.materials.css','glaze.layout.css','glaze.states.css','glaze.workspace.candidate.css',
    'glaze-2.candidate.css','glaze-2.foldable.candidate.css','glaze-2.emerging.candidate.css',
    # Retained 2.1 historical Stable regression/published rollback assets.
    'glaze-2.1.0.css','glaze-2.1.reference.css','glaze-2.1.visual-excellence.css',
    'glaze-2.1.visual-excellence.core.css','glaze-2.1.visual-excellence.review2.css',
    'glaze-2.1.visual-excellence.review3.css','glaze-2.1.visual-excellence.review4.css',
    # Current 2.2 Stable entrypoint and preserved promotion-source layers it imports.
    'glaze-2.2.0.css','glaze-2.2.candidate.css','glaze-2.2.components.candidate.css',
    'glaze-2.2.components.adaptive.candidate.css','glaze-2.2.components.runtime.candidate.css',
    'glaze-2.2.structure.candidate.css','glaze-2.2.overlay.candidate.css','glaze-2.2.advanced.candidate.css',
    'glaze-2.2.visual-refinement.candidate.css','glaze-2.2.optical-reachability.candidate.css',
): shutil.copy2(ROOT/'css'/name,DIST/'assets'/name)
shutil.copy2(IDENTITY/'glaze-ui-mark.svg',DIST/'assets'/'glaze-ui-mark.svg')
print(f'Built {DIST.relative_to(ROOT)} from Glaze UI 2.2.0 Stable source, registry-backed consumer governance, retained 2.1 rollback assets, and synchronized Facet identity')

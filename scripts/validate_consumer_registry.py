#!/usr/bin/env python3
"""Validate the mandatory current-Stable Glaze UI consumer registry."""
from __future__ import annotations
import json,re
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
REGISTRY=ROOT/'consumers'/'registry.json'; DOC=ROOT/'CONSUMERS.md'; VERSION=ROOT/'VERSION'
ALLOWED={'aligned-current-stable','adoption-candidate','migration-required','unverified'}
EXPECTED_REPOS={
    'GoreeCloud/goreecloud-manager',
    'GoreeCloud/goreecloud-website',
    'GoreeCloud/goreecloud-tasks',
    'GoreeCloud/goreecloud-launcher',
    'GoreeCloud/goreecloud-keyboard',
    'GoreeCloud/goreecloud-notes',
    'GoreeCloud/goreecloud-monitor',
    'GoreeCloud/goreecloud-browser',
    'GoreeCloud/goreecloud-wardveil-security',
    'GoreeCloud/goreecloud-privacy-shield',
}
REQUIRED_PLATFORMS={'web','desktop','mobile','tablet','tv','smartwatch','other-user-facing'}
SEMVER=re.compile(r'^\d+\.\d+\.\d+$'); SHA40=re.compile(r'^[0-9a-f]{40}$')
def req(c,m):
    if not c: raise SystemExit(f'Glaze UI consumer registry validation failed: {m}')
def vt(v): req(bool(SEMVER.fullmatch(v)),f'invalid semantic version: {v}'); return tuple(map(int,v.split('.')))
def evidence(n,t,r,e,a): req(isinstance(t,str) and SEMVER.fullmatch(t),f'{n} needs semantic target'); req(isinstance(r,str) and SHA40.fullmatch(r),f'{n} needs reviewed revision'); req(isinstance(e,str) and e.strip(),f'{n} needs evidence'); req(a,f'{n} needs automated contract')
def main():
    req(REGISTRY.is_file() and DOC.is_file() and VERSION.is_file(),'required consumer files missing')
    stable=VERSION.read_text().strip(); data=json.loads(REGISTRY.read_text()); doc=DOC.read_text()
    for m in ('Aligned — current Stable','Adoption Candidate','Migration Required','Unverified','consumers/registry.json','Audit completeness','Mandatory current Stable target','must not silently depend on Candidate or Experimental'): req(m in doc,f'CONSUMERS.md missing {m}')
    req(data.get('schemaVersion')==3,'schemaVersion')
    req(data.get('stableBaseline')==stable,'Stable baseline differs from VERSION')
    req(data.get('requiredConsumerVersion')==stable,'required consumer version differs from VERSION')
    req(set(data.get('statusVocabulary',[]))==ALLOWED,'status vocabulary')
    req(re.fullmatch(r'\d{4}-\d{2}-\d{2}',data.get('auditedAt','')) is not None,'auditedAt')
    historical=data.get('historicalStableVersions')
    req(isinstance(historical,list),'historicalStableVersions must be a list')
    req(all(isinstance(v,str) and SEMVER.fullmatch(v) for v in historical),'historical versions must use semantic versioning')
    req(len(set(historical))==len(historical),'historical Stable versions must be unique')
    req(historical==sorted(historical,key=vt),'historical Stable versions must be ordered')
    req(all(vt(v)<vt(stable) for v in historical),'historical Stable versions must precede current Stable')
    enforcement=data.get('enforcement',{})
    req(enforcement.get('currentStableRequired') is True,'currentStableRequired must be true')
    req(enforcement.get('productionExceptionsAllowed') is False,'production exceptions must be forbidden')
    req(REQUIRED_PLATFORMS.issubset(set(enforcement.get('platformScope',[]))),'platform scope must include web, desktop, mobile, tablet, TV, smartwatch, and other user-facing software')
    req('production-blocked' in enforcement.get('unsupportedPlatformRule',''),'unsupported-platform rule must fail closed')
    consumers=data.get('consumers'); req(isinstance(consumers,list) and consumers,'consumers must be a non-empty list')
    seen=set()
    for c in consumers:
        n=c['name']; repo=c['repository']; s=c['status']; t=c.get('targetVersion'); required=c.get('requiredTargetVersion'); r=c.get('referenceRevision'); e=c.get('evidence'); a=c.get('automatedContract'); eligible=c.get('productionEligible'); acc=c.get('visualAcceptance'); notes=c.get('notes')
        req(repo.startswith('GoreeCloud/') and repo not in seen,f'invalid/duplicate repo {repo}'); seen.add(repo)
        req(s in ALLOWED,f'invalid status {n}')
        req(required==stable,f'{n} required target must equal current Stable {stable}')
        req(isinstance(acc,str) and acc.strip() and isinstance(notes,str) and notes.strip(),f'missing acceptance/notes {n}')
        if s=='aligned-current-stable':
            evidence(n,t,r,e,a); req(t==stable,f'{n} must target current Stable {stable}'); req(eligible is True,f'{n} aligned current Stable must be production eligible')
        elif s=='adoption-candidate':
            evidence(n,t,r,e,a); req(t==stable,f'{n} adoption candidate must target current Stable {stable}'); req(eligible is False,f'{n} candidate must not be production eligible'); req(any(x in acc.lower() for x in ('pending','required','not complete','not established','remains pending')),f'{n} needs incomplete final-acceptance boundary')
        elif s=='migration-required':
            evidence(n,t,r,e,a); req(t in historical,f'{n} migration source target must be a historical Stable release'); req(vt(t)<vt(stable),f'{n} migration source target must precede current Stable'); req(eligible is False,f'{n} migration-required consumer must not be production eligible')
        else:
            req(t is None and r is None and e is None and not a,f'unverified {n} must not claim versioned evidence'); req(eligible is False,f'unverified {n} must not be production eligible')
    req(seen==EXPECTED_REPOS,f'audit scope drift: expected {sorted(EXPECTED_REPOS)}, got {sorted(seen)}')
    print(f'Glaze UI consumer registry validated: {len(consumers)} audited consumers; mandatory current Stable target {stable}')
if __name__=='__main__': main()

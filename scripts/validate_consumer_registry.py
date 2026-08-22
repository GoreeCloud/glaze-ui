#!/usr/bin/env python3
"""Validate the central Glaze UI consumer compatibility registry."""
from __future__ import annotations
import json,re
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
REGISTRY=ROOT/'consumers'/'registry.json'; DOC=ROOT/'CONSUMERS.md'; VERSION=ROOT/'VERSION'
ALLOWED={'aligned-current-stable','aligned-older-stable','adoption-candidate','unverified'}
SEMVER=re.compile(r'^\d+\.\d+\.\d+$'); SHA40=re.compile(r'^[0-9a-f]{40}$')
def req(c,m):
    if not c: raise SystemExit(f'Glaze UI consumer registry validation failed: {m}')
def vt(v): req(bool(SEMVER.fullmatch(v)),f'invalid semantic version: {v}'); return tuple(map(int,v.split('.')))
def evidence(n,t,r,e,a): req(isinstance(t,str) and SEMVER.fullmatch(t),f'{n} needs semantic target'); req(isinstance(r,str) and SHA40.fullmatch(r),f'{n} needs reviewed revision'); req(isinstance(e,str) and e.strip(),f'{n} needs evidence'); req(a,f'{n} needs automated contract')
def main():
    req(REGISTRY.is_file() and DOC.is_file() and VERSION.is_file(),'required consumer files missing')
    stable=VERSION.read_text().strip(); data=json.loads(REGISTRY.read_text()); doc=DOC.read_text()
    for m in ('Aligned — current Stable','Aligned — older Stable','Adoption Candidate','Unverified','consumers/registry.json','must not silently depend on Candidate or Experimental'): req(m in doc,f'CONSUMERS.md missing {m}')
    req(data.get('schemaVersion')==1,'schemaVersion'); req(data.get('stableBaseline')==stable,'Stable baseline differs from VERSION'); req(set(data.get('statusVocabulary',[]))==ALLOWED,'status vocabulary'); req(re.fullmatch(r'\d{4}-\d{2}-\d{2}',data.get('auditedAt','')) is not None,'auditedAt')
    seen=set()
    for c in data['consumers']:
        n=c['name']; repo=c['repository']; s=c['status']; t=c['targetVersion']; r=c['referenceRevision']; e=c['evidence']; a=c['automatedContract']; acc=c['visualAcceptance']; notes=c['notes']
        req(repo.startswith('GoreeCloud/') and repo not in seen,f'invalid/duplicate repo {repo}'); seen.add(repo); req(s in ALLOWED,f'invalid status {n}'); req(isinstance(acc,str) and acc.strip() and isinstance(notes,str) and notes.strip(),f'missing acceptance/notes {n}')
        if s=='aligned-current-stable': evidence(n,t,r,e,a); req(t==stable,f'{n} must target current Stable {stable}')
        elif s=='aligned-older-stable': evidence(n,t,r,e,a); req(vt(t)<vt(stable),f'{n} older-Stable target must be older than {stable}')
        elif s=='adoption-candidate': evidence(n,t,r,e,a); req(vt(t)<=vt(stable),f'{n} adoption target cannot exceed Stable {stable}'); req(any(x in acc.lower() for x in ('pending','required','not complete','not established')),f'{n} needs incomplete final-acceptance boundary')
        else: req(t is None and r is None and e is None and not a,f'unverified {n} must not claim versioned evidence')
    req('GoreeCloud/goreecloud-manager' in seen and 'GoreeCloud/goreecloud-website' in seen,'required audited consumers missing')
    print(f'Glaze UI consumer registry validated: {len(data["consumers"])} audited consumers; Stable baseline {stable}')
if __name__=='__main__': main()

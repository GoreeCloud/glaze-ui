#!/usr/bin/env python3
"""Validate mandatory Glaze UI 2.1 Stable consumer migration state."""
from __future__ import annotations
import json,re
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
SEMVER=re.compile(r'^\d+\.\d+\.\d+$'); SHA40=re.compile(r'^[0-9a-f]{40}$')
EXPECTED={"GoreeCloud/goreecloud-manager","GoreeCloud/goreecloud-website","GoreeCloud/goreecloud-tasks","GoreeCloud/goreecloud-launcher","GoreeCloud/goreecloud-keyboard","GoreeCloud/goreecloud-notes","GoreeCloud/goreecloud-monitor","GoreeCloud/goreecloud-browser","GoreeCloud/goreecloud-wardveil-security","GoreeCloud/goreecloud-privacy-shield"}
def req(c,m):
    if not c: raise SystemExit(f'Glaze UI consumer registry validation failed: {m}')
def vt(v): return tuple(map(int,v.split('.')))
def main():
    stable=(ROOT/'VERSION').read_text().strip(); req(stable=='2.1.0','Stable must be 2.1.0')
    data=json.loads((ROOT/'consumers/registry.json').read_text()); lifecycle=json.loads((ROOT/'registry/lifecycle.json').read_text())
    req(data.get('schemaVersion')==4,'schemaVersion'); req(data.get('stableBaseline')==stable and data.get('requiredConsumerVersion')==stable,'Stable target')
    historical=data.get('historicalStableVersions',[]); req('2.0.0' in historical and all(SEMVER.fullmatch(v) for v in historical),'historical Stable list'); req(all(vt(v)<vt(stable) for v in historical),'historical versions must precede Stable')
    req(lifecycle.get('currentStable')==stable and lifecycle.get('activeCandidate') is None,'lifecycle Stable state')
    stable_release=[r for r in lifecycle.get('releases',[]) if r.get('version')==stable]; req(len(stable_release)==1 and stable_release[0].get('status')=='stable','Stable release record')
    promoted=stable_release[0].get('promotedFromCandidate'); req(promoted=='2.1.0-candidate.1','promotion source')
    assessment=data.get('candidateAssessment',{}); req(assessment.get('version')==promoted and assessment.get('lifecycle')=='candidate','preserved Candidate assessment'); req(assessment.get('consumerEligible') is False and assessment.get('productionEligible') is False,'Candidate assessment boundary')
    consumers=data.get('consumers',[]); seen=set()
    for c in consumers:
        repo=c.get('repository'); req(repo in EXPECTED and repo not in seen,f'invalid/duplicate {repo}'); seen.add(repo)
        req(c.get('requiredTargetVersion')==stable,f'{repo} required target'); req(c.get('productionEligible') is False,f'{repo} must not auto-promote')
        status=c.get('status'); target=c.get('targetVersion')
        if status=='migration-required':
            req(isinstance(target,str) and target in historical,f'{repo} migration source'); req(SHA40.fullmatch(str(c.get('referenceRevision',''))) is not None,f'{repo} revision'); req(c.get('automatedContract') is True and c.get('evidence'),f'{repo} evidence')
        elif status=='unverified':
            req(target is None and c.get('referenceRevision') is None and c.get('evidence') is None and c.get('automatedContract') is False,f'{repo} unverified boundary')
        else: req(False,f'{repo} must remain migration-required or unverified immediately after Stable promotion')
    req(seen==EXPECTED,'audit scope drift')
    print(f'Glaze UI consumer registry validated: {len(consumers)} consumers require Stable {stable}; none auto-promoted')
if __name__=='__main__': main()

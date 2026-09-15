#!/usr/bin/env node
import {execFileSync} from 'node:child_process';
import {readFileSync, writeFileSync} from 'node:fs';
import {resolve} from 'node:path';

const HEX40 = /^[0-9a-f]{40}$/;
const REPOSITORY = 'GoreeCloud/goreecloud-glaze-ui';

const ALLOWED_RELEASE_PATHS = new Set([
  '.github/workflows/glaze-v1.4.1-promotion-gate.yml',
  '.github/workflows/glaze-v1.4.1-stable.yml',
  'ACCEPTANCE.md',
  'ADOPTION.md',
  'CONFORMANCE.md',
  'CONSUMERS.md',
  'CONTRIBUTING.md',
  'ENFORCEMENT.md',
  'GLAZE_UI_V1_4_1.md',
  'ICON_CONSTRUCTION.md',
  'ICON_IDENTITY.md',
  'README.md',
  'STABILITY.md',
  'VERSION',
  'acceptance/v1.4.1-stable.md',
  'consumers/registry.json',
  'css/glaze-v1.4.1.css',
  'js/glaze-v1.4.1-optical-engine.mjs',
  'js/glaze-v1.4.1.mjs',
  'reference/v1.4.1/README.md',
  'registry/lifecycle.json',
  'scripts/prepare_glaze_v1_4_1_release_continuity.mjs',
  'scripts/verify_glaze_v1_4_1_human_validation.mjs',
  'scripts/verify_glaze_v1_4_1_optical_runtime.mjs',
  'scripts/verify_glaze_v1_4_1_stable.mjs',
  'scripts/verify_glaze_v1_4_stable.mjs',
  'website/404.html',
  'website/README.md',
  'website/index.html'
]);

const IMMUTABLE_BASELINE_PATHS = [
  'css/glaze-v1.4.0.css',
  'js/glaze-v1.4.0.mjs',
  'js/glaze-v1.4-optical-engine.mjs'
];

const PROMOTED_BLOB_PAIRS = [
  ['css/glaze-v1.4.1.candidate.css', 'css/glaze-v1.4.1.css'],
  ['js/glaze-v1.4.1-optical-engine.candidate.mjs', 'js/glaze-v1.4.1-optical-engine.mjs']
];

class ContinuityError extends Error {}

function requireCondition(condition, message) {
  if (!condition) throw new ContinuityError(message);
}

function parseArgs(argv) {
  const args = {record: null, sourceAnchor: null, targetRevision: null, output: null};
  for (let index = 0; index < argv.length; index += 1) {
    const arg = argv[index];
    if (arg === '--record') args.record = argv[++index];
    else if (arg === '--source-anchor') args.sourceAnchor = argv[++index];
    else if (arg === '--target-revision') args.targetRevision = argv[++index];
    else if (arg === '--output') args.output = argv[++index];
    else throw new ContinuityError(`unknown argument ${arg}`);
  }
  requireCondition(args.record, '--record is required');
  requireCondition(args.output, '--output is required');
  requireCondition(HEX40.test(args.sourceAnchor || ''), '--source-anchor must be 40 lowercase hex characters');
  requireCondition(HEX40.test(args.targetRevision || ''), '--target-revision must be 40 lowercase hex characters');
  requireCondition(args.sourceAnchor !== args.targetRevision, 'release continuity requires different source and target revisions');
  return args;
}

function git(args) {
  return execFileSync('git', args, {encoding: 'utf8'}).trim();
}

function gitBlob(revision, path) {
  return git(['rev-parse', `${revision}:${path}`]);
}

function loadJson(path) {
  const value = JSON.parse(readFileSync(resolve(path), 'utf8'));
  requireCondition(value && typeof value === 'object' && !Array.isArray(value), `${path} must contain a JSON object`);
  return value;
}

function positiveEvidence(record) {
  const items = [];
  for (const session of record.sessions || []) {
    const sourceRevision = session?.build?.sourceRevision;
    for (const result of session?.results || []) {
      if (result?.status === 'pass' || result?.status === 'not_applicable') {
        items.push({checkId: result.id, sourceRevision, authorityId: session.id, kind: 'session'});
      }
    }
  }
  for (const item of record.legacyEvidence || []) {
    if (item?.status === 'pass' || item?.status === 'not_applicable') {
      items.push({checkId: item.checkId, sourceRevision: item.sourceRevision, authorityId: item.id, kind: 'legacy'});
    }
  }
  return items;
}

function existingContinuity(record) {
  const map = new Map();
  for (const assessment of record.continuityAssessments || []) {
    for (const checkId of assessment?.checkIds || []) {
      map.set(`${assessment.sourceRevision}:${assessment.targetRevision}:${checkId}`, assessment);
    }
  }
  return map;
}

function changedPaths(sourceAnchor, targetRevision) {
  const raw = git(['diff', '--name-status', '--find-renames', sourceAnchor, targetRevision]);
  if (!raw) return [];
  return raw.split('\n').map(line => {
    const parts = line.split('\t');
    const status = parts[0];
    const path = parts.at(-1);
    requireCondition(/^[AM]$/.test(status), `release continuity refuses non-add/modify change ${status} for ${path}`);
    return path;
  });
}

function verifyReleaseDelta(sourceAnchor, targetRevision) {
  try {
    execFileSync('git', ['merge-base', '--is-ancestor', sourceAnchor, targetRevision], {stdio: 'ignore'});
  } catch {
    throw new ContinuityError(`${sourceAnchor} is not an ancestor of ${targetRevision}`);
  }

  const paths = changedPaths(sourceAnchor, targetRevision);
  requireCondition(paths.length > 0, 'release continuity requires a non-empty release delta');
  for (const path of paths) {
    requireCondition(ALLOWED_RELEASE_PATHS.has(path), `release continuity refuses behavior-unknown changed path: ${path}`);
  }

  for (const path of IMMUTABLE_BASELINE_PATHS) {
    const sourceBlob = gitBlob(sourceAnchor, path);
    const targetBlob = gitBlob(targetRevision, path);
    requireCondition(sourceBlob === targetBlob, `V1.4.0 immutable baseline changed at ${path}`);
  }

  for (const [candidatePath, stablePath] of PROMOTED_BLOB_PAIRS) {
    const candidateBlob = gitBlob(sourceAnchor, candidatePath);
    const stableBlob = gitBlob(targetRevision, stablePath);
    requireCondition(candidateBlob === stableBlob, `promoted Stable blob differs from qualified Candidate: ${candidatePath} -> ${stablePath}`);
  }

  return paths;
}

function buildContinuity(record, contract, sourceAnchor, targetRevision, releasePaths) {
  requireCondition(record.repository === REPOSITORY, `record repository must be ${REPOSITORY}`);
  requireCondition(record.decision === 'accepted', 'source promotion record must remain accepted');
  requireCondition(record.promotionEligible === true, 'source promotion record must remain promotionEligible=true');

  const positives = positiveEvidence(record);
  const continuity = existingContinuity(record);
  const requiredChecks = contract.requiredChecks.map(item => item.id);
  const grouped = new Map();

  for (const checkId of requiredChecks) {
    const candidates = positives.filter(item => item.checkId === checkId && HEX40.test(item.sourceRevision || ''));
    let selected = candidates.find(item => item.sourceRevision === sourceAnchor);
    let prior = null;
    if (!selected) {
      selected = candidates.find(item => {
        const assessment = continuity.get(`${item.sourceRevision}:${sourceAnchor}:${checkId}`);
        if (assessment?.decision === 'unaffected') {
          prior = assessment;
          return true;
        }
        return false;
      });
    }
    requireCondition(selected, `no positive human authority with approved continuity to source anchor for ${checkId}`);

    const key = selected.sourceRevision;
    if (!grouped.has(key)) grouped.set(key, {checkIds: [], priorAssessments: new Map()});
    const group = grouped.get(key);
    group.checkIds.push(checkId);
    if (selected.sourceRevision !== sourceAnchor) {
      const assessment = prior || continuity.get(`${selected.sourceRevision}:${sourceAnchor}:${checkId}`);
      requireCondition(assessment?.decision === 'unaffected', `missing approved source-to-anchor continuity for ${checkId}`);
      group.priorAssessments.set(assessment.id, assessment);
    }
  }

  const now = new Date().toISOString();
  const compareRef = `https://github.com/${REPOSITORY}/compare/${sourceAnchor}...${targetRevision}`;
  const candidateCssRef = `https://github.com/${REPOSITORY}/blob/${sourceAnchor}/css/glaze-v1.4.1.candidate.css`;
  const stableCssRef = `https://github.com/${REPOSITORY}/blob/${targetRevision}/css/glaze-v1.4.1.css`;
  const candidateOpticsRef = `https://github.com/${REPOSITORY}/blob/${sourceAnchor}/js/glaze-v1.4.1-optical-engine.candidate.mjs`;
  const stableOpticsRef = `https://github.com/${REPOSITORY}/blob/${targetRevision}/js/glaze-v1.4.1-optical-engine.mjs`;

  const generated = [];
  for (const [sourceRevision, group] of grouped.entries()) {
    const priorPaths = [...group.priorAssessments.values()].flatMap(item => item.changedPathsReviewed || []);
    const priorRefs = [...group.priorAssessments.values()].flatMap(item => item.evidenceRefs || []);
    const changedPathsReviewed = [...new Set([...priorPaths, ...releasePaths])].sort();
    const evidenceRefs = [...new Set([...priorRefs, compareRef, candidateCssRef, stableCssRef, candidateOpticsRef, stableOpticsRef])];
    const chained = sourceRevision === sourceAnchor
      ? 'The qualified implementation anchor is the historical evidence source for these checks.'
      : 'The governed record already contains approved unaffected continuity from this historical evidence source to the qualified implementation anchor.';

    generated.push({
      id: `release-continuity-${sourceRevision.slice(0, 12)}-${targetRevision.slice(0, 12)}`,
      assessedAt: now,
      assessor: 'GoreeCloud V1.4.1 exact-revision release continuity gate',
      assessorRole: 'release-governance source-impact verifier',
      sourceRevision,
      targetRevision,
      checkIds: [...group.checkIds].sort(),
      decision: 'unaffected',
      rationale: `${chained} The anchor-to-target release delta is restricted to governed release authority, documentation, consumer targeting, verification automation, a Stable metadata/alias entrypoint, and byte-identical promotion of the reviewed V1.4.1 CSS and optical-engine blobs. V1.4.0 baseline blobs are unchanged. No reviewed behavior for these checks changes across the resulting exact source-to-target path. This continuity assessment is release-governance evidence only and does not relabel historical human evidence as target-revision testing.`,
      changedPathsReviewed,
      evidenceRefs
    });
  }

  const existingKeys = new Set((record.continuityAssessments || []).flatMap(item =>
    (item.checkIds || []).map(checkId => `${item.sourceRevision}:${item.targetRevision}:${checkId}`)
  ));
  for (const assessment of generated) {
    for (const checkId of assessment.checkIds) {
      requireCondition(!existingKeys.has(`${assessment.sourceRevision}:${assessment.targetRevision}:${checkId}`), `target continuity already exists for ${checkId} from ${assessment.sourceRevision}`);
    }
  }

  return generated;
}

function main() {
  const args = parseArgs(process.argv.slice(2));
  const record = loadJson(args.record);
  const contract = loadJson('contracts/v1.4.1/human-validation.contract.json');
  requireCondition(Array.isArray(contract.requiredChecks) && contract.requiredChecks.length === 34, 'canonical V1.4.1 contract must contain 34 checks');

  const releasePaths = verifyReleaseDelta(args.sourceAnchor, args.targetRevision);
  const generated = buildContinuity(record, contract, args.sourceAnchor, args.targetRevision, releasePaths);
  requireCondition(generated.length > 0, 'no release continuity assessments were generated');

  const output = structuredClone(record);
  output.continuityAssessments = [...(record.continuityAssessments || []), ...generated];
  writeFileSync(resolve(args.output), `${JSON.stringify(output, null, 2)}\n`, {flag: 'wx'});

  console.log(`Prepared exact-revision V1.4.1 release continuity for ${args.targetRevision}.`);
  console.log(`Qualified source anchor: ${args.sourceAnchor}`);
  console.log(`Release paths reviewed: ${releasePaths.length}`);
  console.log(`Generated continuity assessments: ${generated.length}`);
  console.log('Boundary: continuity preserves already-valid human authority; it is not new human evidence.');
}

try {
  main();
} catch (error) {
  console.error(`GLAZE UI V1.4.1 release continuity preparation failed: ${error?.message || error}`);
  process.exit(1);
}

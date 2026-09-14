#!/usr/bin/env node
import assert from 'node:assert/strict';
import {readFileSync} from 'node:fs';
import {resolve, isAbsolute} from 'node:path';
import {fileURLToPath} from 'node:url';

const ROOT = fileURLToPath(new URL('../', import.meta.url));
const CONTRACT_PATH = 'contracts/v1.4.1/human-validation.contract.json';
const TEMPLATE_PATH = 'acceptance/v1.4.1-human-validation.template.json';
const HEX40 = /^[0-9a-f]{40}$/;
const PLACEHOLDERS = new Set(['', 'todo', 'tbd', 'unknown', 'n/a', 'na', 'placeholder', 'example', 'none', 'null']);
const SYNTHETIC_REVIEWER = /^(synthetic|test|example|ci|automation)/i;

class HumanValidationError extends Error {}

function req(condition, message) {
  if (!condition) throw new HumanValidationError(message);
}

function read(relativeOrAbsolute) {
  const path = isAbsolute(relativeOrAbsolute) ? relativeOrAbsolute : resolve(ROOT, relativeOrAbsolute);
  return readFileSync(path, 'utf8');
}

function json(path) {
  let value;
  try {
    value = JSON.parse(read(path));
  } catch (error) {
    throw new HumanValidationError(`invalid JSON ${path}: ${error.message}`);
  }
  req(value && typeof value === 'object' && !Array.isArray(value), `${path} must contain a JSON object`);
  return value;
}

function meaningful(value, label) {
  req(typeof value === 'string', `${label} must be a string`);
  const text = value.trim();
  req(!PLACEHOLDERS.has(text.toLowerCase()), `${label} contains a placeholder value`);
  req(!text.includes('REPLACE_WITH_'), `${label} contains an unresolved template placeholder`);
  return text;
}

function timestamp(value, label) {
  const text = meaningful(value, label);
  req(/(?:Z|[+-]\d{2}:\d{2})$/.test(text), `${label} must include an explicit timezone`);
  req(!Number.isNaN(Date.parse(text)), `${label} must be ISO-8601`);
  return text;
}

function stringArray(value, label, {allowEmpty = true} = {}) {
  req(Array.isArray(value), `${label} must be an array`);
  if (!allowEmpty) req(value.length > 0, `${label} must not be empty`);
  for (let index = 0; index < value.length; index += 1) meaningful(value[index], `${label}[${index}]`);
  return value;
}

function validateSource() {
  const contract = json(CONTRACT_PATH);
  const template = json(TEMPLATE_PATH);
  const lifecycle = json('registry/lifecycle.json');

  assert.equal(lifecycle.currentStable, '1.4.0', 'V1.4.1 hardening must preserve V1.4.0 Stable authority');
  assert.equal(lifecycle.currentOfficial, '1.4.0', 'V1.4.1 hardening must preserve V1.4.0 Official authority');
  assert.equal(lifecycle.plannedNext, '1.4.1-candidate', 'lifecycle plannedNext must remain 1.4.1-candidate');
  assert.equal(contract.version, '1.4.1-candidate');
  assert.equal(contract.baselineVersion, '1.4.0');
  assert.equal(contract.lifecycle, 'planned-follow-up');
  assert.equal(contract.evidenceAuthority, 'human');
  assert.equal(contract.rules?.automatedEvidenceMaySupportButNeverSatisfyHumanAuthority, true);
  assert.equal(contract.rules?.promotionRequiresNoPendingBlockedOrFailedChecks, true);
  assert.equal(contract.rules?.v140EvidenceMustNotBeRewritten, true);

  const required = contract.requiredChecks;
  req(Array.isArray(required) && required.length > 0, 'contract must enumerate requiredChecks');
  const ids = required.map((item, index) => meaningful(item?.id, `requiredChecks[${index}].id`));
  req(new Set(ids).size === ids.length, 'requiredChecks ids must be unique');
  for (let index = 0; index < required.length; index += 1) {
    meaningful(required[index].category, `requiredChecks[${index}].category`);
    meaningful(required[index].description, `requiredChecks[${index}].description`);
  }

  assert.equal(template.recordType, 'glaze-v1.4.1-human-validation');
  assert.equal(template.glazeUiVersion, '1.4.1');
  assert.equal(template.baselineVersion, '1.4.0');
  assert.equal(template.evidenceType, 'human');
  assert.deepEqual(template.sessions, [], 'template must not manufacture human review sessions');
  assert.equal(template.decision, 'pending', 'template must fail closed');
  assert.equal(template.promotionEligible, false, 'template must never be promotion eligible');

  const hardening = read('GLAZE_UI_V1_4_1_HARDENING.md');
  assert.match(hardening, /Automated evidence may support a review but must not be relabeled as human evidence/i);
  assert.match(hardening, /v1\.4\.1-human-validation\.template\.json/i);
  assert.match(hardening, /verify_glaze_v1_4_1_human_validation\.mjs/i);
  return contract;
}

function validateEnvironment(environment, label) {
  req(environment && typeof environment === 'object' && !Array.isArray(environment), `${label} must be an object`);
  meaningful(environment.platform, `${label}.platform`);
  meaningful(environment.osVersion, `${label}.osVersion`);
  meaningful(environment.device, `${label}.device`);
  meaningful(environment.formFactor, `${label}.formFactor`);
  meaningful(environment.display, `${label}.display`);
  stringArray(environment.inputModalities, `${label}.inputModalities`);
  stringArray(environment.assistiveTechnologies, `${label}.assistiveTechnologies`);
}

function validateRecord(record, contract, options = {}) {
  const {promotion = false, expectedRevision = null, allowSynthetic = false} = options;
  assert.equal(record.schemaVersion, 1, 'record schemaVersion must be 1');
  assert.equal(record.recordType, 'glaze-v1.4.1-human-validation', 'recordType mismatch');
  assert.equal(record.glazeUiVersion, '1.4.1', 'glazeUiVersion must be 1.4.1');
  assert.equal(record.baselineVersion, '1.4.0', 'baselineVersion must be 1.4.0');
  assert.equal(record.repository, 'GoreeCloud/goreecloud-glaze-ui', 'repository mismatch');
  assert.equal(record.evidenceType, 'human', 'record evidenceType must be human');
  req(Array.isArray(record.sessions) && record.sessions.length > 0, 'record must contain at least one human review session');
  req(Array.isArray(record.exceptions), 'exceptions must be an array');
  stringArray(record.exceptions, 'exceptions');
  meaningful(record.summary, 'summary');

  if (promotion) {
    req(typeof expectedRevision === 'string' && HEX40.test(expectedRevision), '--promotion requires an explicit 40-character --expected-revision');
    req(record.decision === 'accepted', 'promotion record decision must be accepted');
    req(record.promotionEligible === true, 'promotion record must explicitly set promotionEligible=true');
    req(record.exceptions.length === 0, 'promotion record cannot contain unresolved exceptions');
  } else {
    req(['pending', 'accepted', 'rejected'].includes(record.decision), 'decision must be pending, accepted, or rejected');
    req(typeof record.promotionEligible === 'boolean', 'promotionEligible must be boolean');
  }

  const requiredIds = new Set(contract.requiredChecks.map(item => item.id));
  const resultsById = new Map([...requiredIds].map(id => [id, []]));
  const sessionIds = new Set();

  for (let sessionIndex = 0; sessionIndex < record.sessions.length; sessionIndex += 1) {
    const session = record.sessions[sessionIndex];
    const prefix = `sessions[${sessionIndex}]`;
    req(session && typeof session === 'object' && !Array.isArray(session), `${prefix} must be an object`);
    const sessionId = meaningful(session.id, `${prefix}.id`);
    req(!sessionIds.has(sessionId), `${prefix}.id must be unique`);
    sessionIds.add(sessionId);
    timestamp(session.reviewedAt, `${prefix}.reviewedAt`);
    const reviewer = meaningful(session.reviewer, `${prefix}.reviewer`);
    meaningful(session.reviewerRole, `${prefix}.reviewerRole`);
    if (!allowSynthetic) req(!SYNTHETIC_REVIEWER.test(reviewer), `${prefix}.reviewer must identify a real human reviewer, not synthetic/automation evidence`);

    req(session.build && typeof session.build === 'object' && !Array.isArray(session.build), `${prefix}.build must be an object`);
    const revision = meaningful(session.build.sourceRevision, `${prefix}.build.sourceRevision`);
    req(HEX40.test(revision), `${prefix}.build.sourceRevision must be 40 lowercase hex characters`);
    if (expectedRevision) req(revision === expectedRevision, `${prefix} reviewed ${revision}; expected exact revision ${expectedRevision}`);
    meaningful(session.build.artifact, `${prefix}.build.artifact`);
    meaningful(session.build.buildIdentifier, `${prefix}.build.buildIdentifier`);
    validateEnvironment(session.environment, `${prefix}.environment`);

    req(Array.isArray(session.results) && session.results.length > 0, `${prefix}.results must contain at least one result`);
    const localIds = new Set();
    for (let resultIndex = 0; resultIndex < session.results.length; resultIndex += 1) {
      const result = session.results[resultIndex];
      const rlabel = `${prefix}.results[${resultIndex}]`;
      req(result && typeof result === 'object' && !Array.isArray(result), `${rlabel} must be an object`);
      const id = meaningful(result.id, `${rlabel}.id`);
      req(requiredIds.has(id), `${rlabel}.id is not defined by the V1.4.1 human-validation contract`);
      req(!localIds.has(id), `${prefix} contains duplicate result ${id}`);
      localIds.add(id);
      req(['pass', 'fail', 'blocked', 'not_applicable', 'pending'].includes(result.status), `${rlabel}.status is invalid`);
      meaningful(result.scope, `${rlabel}.scope`);
      stringArray(result.limitations, `${rlabel}.limitations`);
      stringArray(result.evidenceRefs, `${rlabel}.evidenceRefs`);

      if (result.status === 'pending') {
        req(!promotion, `${id} is pending and cannot satisfy promotion`);
      } else {
        meaningful(result.finding, `${rlabel}.finding`);
        if (result.status === 'pass' || result.status === 'fail') {
          req(result.evidenceRefs.length > 0, `${id} ${result.status} requires at least one evidence reference`);
        }
        if (result.status === 'not_applicable') {
          req(result.finding.trim().length >= 12, `${id} not_applicable requires an explicit rationale`);
        }
      }
      resultsById.get(id).push({status: result.status, sessionId, revision});
    }
  }

  for (const [id, results] of resultsById.entries()) {
    req(results.length > 0, `required human-validation check ${id} is missing from all sessions`);
    if (promotion) {
      const statuses = new Set(results.map(item => item.status));
      req(!statuses.has('fail'), `${id} contains a failed result`);
      req(!statuses.has('blocked'), `${id} contains a blocked result`);
      req(!statuses.has('pending'), `${id} contains a pending result`);
      req(statuses.has('pass') || statuses.has('not_applicable'), `${id} has no promotable result`);
    }
  }

  if (record.decision === 'accepted') {
    for (const [id, results] of resultsById.entries()) {
      req(results.length > 0, `accepted record is missing ${id}`);
      req(results.every(item => !['fail', 'blocked', 'pending'].includes(item.status)), `accepted record contains unresolved ${id}`);
    }
    req(record.exceptions.length === 0, 'accepted record cannot contain unresolved exceptions');
  }

  if (record.decision === 'rejected') {
    const hasNegative = [...resultsById.values()].flat().some(item => ['fail', 'blocked'].includes(item.status));
    req(hasNegative || record.exceptions.length > 0, 'rejected record must identify a failed/blocked check or exception');
    req(record.promotionEligible === false, 'rejected record cannot be promotion eligible');
  }

  if (record.promotionEligible === true) {
    req(record.decision === 'accepted', 'promotionEligible=true requires decision=accepted');
  }

  return {
    sessions: record.sessions.length,
    coveredChecks: [...resultsById.values()].filter(items => items.length > 0).length,
    requiredChecks: requiredIds.size
  };
}

function syntheticRecord(contract, revision = 'a'.repeat(40)) {
  return {
    schemaVersion: 1,
    recordType: 'glaze-v1.4.1-human-validation',
    glazeUiVersion: '1.4.1',
    baselineVersion: '1.4.0',
    repository: 'GoreeCloud/goreecloud-glaze-ui',
    evidenceType: 'human',
    sessions: [{
      id: 'synthetic-format-self-test',
      reviewedAt: '2026-09-13T19:00:00-05:00',
      reviewer: 'synthetic-self-test',
      reviewerRole: 'validator-self-test',
      build: {sourceRevision: revision, artifact: 'synthetic-artifact', buildIdentifier: 'synthetic-build'},
      environment: {
        platform: 'synthetic-platform',
        osVersion: 'synthetic-os',
        device: 'synthetic-device',
        formFactor: 'synthetic-form-factor',
        display: 'synthetic-display',
        inputModalities: [],
        assistiveTechnologies: []
      },
      results: contract.requiredChecks.map(check => ({
        id: check.id,
        status: 'pass',
        scope: 'Synthetic structural self-test only; not human evidence.',
        finding: 'Synthetic pass used only to exercise validator structure; it is not acceptance evidence.',
        limitations: [],
        evidenceRefs: ['synthetic://not-human-evidence']
      }))
    }],
    exceptions: [],
    decision: 'accepted',
    promotionEligible: true,
    summary: 'Synthetic structural validator self-test only; never human acceptance evidence.'
  };
}

function expectReject(record, contract, options, label) {
  try {
    validateRecord(record, contract, options);
  } catch (error) {
    if (error instanceof HumanValidationError || error instanceof assert.AssertionError) return;
    throw error;
  }
  throw new HumanValidationError(`self-test expected rejection for ${label}`);
}

function clone(value) {
  return JSON.parse(JSON.stringify(value));
}

function selfTest(contract) {
  const revision = 'a'.repeat(40);
  const valid = syntheticRecord(contract, revision);
  validateRecord(valid, contract, {promotion: true, expectedRevision: revision, allowSynthetic: true});

  const automated = clone(valid);
  automated.evidenceType = 'automated';
  expectReject(automated, contract, {allowSynthetic: true}, 'automated evidence authority substitution');

  const missing = clone(valid);
  missing.sessions[0].results.pop();
  expectReject(missing, contract, {allowSynthetic: true}, 'missing required check');

  const pending = clone(valid);
  pending.sessions[0].results[0].status = 'pending';
  pending.sessions[0].results[0].finding = null;
  pending.sessions[0].results[0].evidenceRefs = [];
  expectReject(pending, contract, {promotion: true, expectedRevision: revision, allowSynthetic: true}, 'pending promotion check');

  const failed = clone(valid);
  failed.sessions[0].results[0].status = 'fail';
  expectReject(failed, contract, {promotion: true, expectedRevision: revision, allowSynthetic: true}, 'failed promotion check');

  const stale = clone(valid);
  stale.sessions[0].build.sourceRevision = 'b'.repeat(40);
  expectReject(stale, contract, {promotion: true, expectedRevision: revision, allowSynthetic: true}, 'stale tested revision');

  const noEvidence = clone(valid);
  noEvidence.sessions[0].results[0].evidenceRefs = [];
  expectReject(noEvidence, contract, {allowSynthetic: true}, 'pass without evidence reference');

  const fakeReviewer = clone(valid);
  expectReject(fakeReviewer, contract, {}, 'synthetic reviewer in real record mode');

  const naWithoutRationale = clone(valid);
  naWithoutRationale.sessions[0].results[0].status = 'not_applicable';
  naWithoutRationale.sessions[0].results[0].finding = 'N/A';
  naWithoutRationale.sessions[0].results[0].evidenceRefs = [];
  expectReject(naWithoutRationale, contract, {allowSynthetic: true}, 'not-applicable without rationale');
}

function parseArgs(argv) {
  const args = {record: null, promotion: false, expectedRevision: null, selfTest: false, sourceOnly: false};
  for (let index = 0; index < argv.length; index += 1) {
    const arg = argv[index];
    if (arg === '--record') args.record = argv[++index];
    else if (arg === '--promotion') args.promotion = true;
    else if (arg === '--expected-revision') args.expectedRevision = argv[++index];
    else if (arg === '--self-test') args.selfTest = true;
    else if (arg === '--source-only') args.sourceOnly = true;
    else throw new HumanValidationError(`unknown argument ${arg}`);
  }
  if (args.promotion && !args.record) throw new HumanValidationError('--promotion requires --record');
  return args;
}

function main() {
  const args = parseArgs(process.argv.slice(2));
  const contract = validateSource();
  console.log(`GLAZE UI V1.4.1 human-validation source protocol passed (${contract.requiredChecks.length} required checks).`);

  if (args.selfTest) {
    selfTest(contract);
    console.log('Synthetic V1.4.1 validator self-test passed. Synthetic records are not human evidence.');
  }

  if (args.record) {
    const record = json(resolve(process.cwd(), args.record));
    const summary = validateRecord(record, contract, {promotion: args.promotion, expectedRevision: args.expectedRevision});
    console.log(`Validated human record: ${summary.sessions} session(s), ${summary.coveredChecks}/${summary.requiredChecks} required checks covered.`);
    if (args.promotion) console.log(`V1.4.1 human-validation promotion gate passed for exact revision ${args.expectedRevision}.`);
  }

  if (!args.record && !args.selfTest && !args.sourceOnly) {
    console.log('No human record supplied; V1.4.1 human acceptance remains pending.');
  }
}

try {
  main();
} catch (error) {
  if (error instanceof HumanValidationError || error instanceof assert.AssertionError) {
    console.error(`GLAZE UI V1.4.1 human-validation verification failed: ${error.message}`);
    process.exit(1);
  }
  throw error;
}

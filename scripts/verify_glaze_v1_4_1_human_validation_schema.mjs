#!/usr/bin/env node
import assert from 'node:assert/strict';
import {readFileSync} from 'node:fs';

function json(path) {
  return JSON.parse(readFileSync(new URL(`../${path}`, import.meta.url), 'utf8'));
}

const contract = json('contracts/v1.4.1/human-validation.contract.json');
const schema = json('schemas/v1.4.1-human-validation-record.schema.json');
const template = json('acceptance/v1.4.1-human-validation.template.json');

assert.equal(schema.$schema, 'https://json-schema.org/draft/2020-12/schema');
assert.equal(schema.type, 'object');
assert.equal(schema.additionalProperties, false);
assert.equal(schema.properties?.schemaVersion?.const, 1);
assert.equal(schema.properties?.recordType?.const, 'glaze-v1.4.1-human-validation');
assert.equal(schema.properties?.glazeUiVersion?.const, '1.4.1');
assert.equal(schema.properties?.baselineVersion?.const, '1.4.0');
assert.equal(schema.properties?.repository?.const, 'GoreeCloud/goreecloud-glaze-ui');
assert.equal(schema.properties?.evidenceType?.const, 'human');
assert.deepEqual(schema.properties?.decision?.enum, ['pending', 'accepted', 'rejected']);
assert.equal(schema.properties?.promotionEligible?.type, 'boolean');

const contractIds = contract.requiredChecks.map(item => item.id).sort();
const schemaIds = [...schema.$defs.result.properties.id.enum].sort();
assert.equal(new Set(contractIds).size, contractIds.length, 'contract required-check ids must be unique');
assert.equal(new Set(schemaIds).size, schemaIds.length, 'schema result ids must be unique');
assert.deepEqual(schemaIds, contractIds, 'record schema required-check ids must exactly match the contract');

assert.equal(template.recordType, schema.properties.recordType.const);
assert.equal(template.glazeUiVersion, schema.properties.glazeUiVersion.const);
assert.equal(template.baselineVersion, schema.properties.baselineVersion.const);
assert.equal(template.repository, schema.properties.repository.const);
assert.equal(template.evidenceType, schema.properties.evidenceType.const);
assert.deepEqual(template.sessions, [], 'template must remain deliberately empty and fail closed');
assert.equal(template.decision, 'pending');
assert.equal(template.promotionEligible, false);

console.log(`GLAZE UI V1.4.1 human-validation schema parity passed (${contractIds.length} canonical checks).`);
console.log('Schema validation proves structure/parity only; it is not human acceptance evidence.');

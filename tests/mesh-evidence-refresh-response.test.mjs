import test from "node:test";
import assert from "node:assert/strict";
import { normalizeMeshEvidenceRefreshResponse } from "../reference/mesh-evidence-refresh-response.mjs";

const now = new Date("2026-08-27T20:05:00.000Z");

function response(overrides = {}) {
  return {
    version: "goreecloud.evidence-refresh-response.v1",
    id: "wardveil-refresh-response-001",
    intent: {
      id: "refresh-wardveil-drive-001",
      coordinator_revision: "a".repeat(40),
      reason: "stale",
      requested_at: "2026-08-27T20:00:00.000Z",
    },
    producer: {
      system: "wardveil-security",
      repository: "GoreeCloud/goreecloud-wardveil-security",
      revision: "b".repeat(40),
    },
    authority_domain: "security",
    subject: { kind: "service", id: "goreecloud-drive", scope: "runtime" },
    assertion: "security-status",
    status: "completed",
    reason_code: "evidence-issued",
    responded_at: "2026-08-27T20:04:00.000Z",
    evidence_produced: true,
    evidence_envelope_id: "wardveil-evidence-002",
    contains_user_content: false,
    contains_secret_material: false,
    authority_transferred: false,
    execution_authorized: false,
    ...overrides,
  };
}

test("presents completed handling without promoting the receipt to current evidence", () => {
  const model = normalizeMeshEvidenceRefreshResponse(response(), { now });
  assert.equal(model.kind, "evidence-refresh-response");
  assert.equal(model.handling.status, "completed");
  assert.equal(model.handling.completed, true);
  assert.equal(model.evidence_reference.envelope_id, "wardveil-evidence-002");
  assert.equal(model.evidence_reference.validation_required, true);
  assert.equal(model.current_evidence_established, false);
  assert.equal(model.producer_authority_preserved, true);
  assert.equal(model.execution_authorized, false);
  assert.equal("outcome" in model, false);
  assert.equal("verdict" in model, false);
  assert.equal("fresh" in model, false);
});

test("presents completed handling with no evidence as no evidence reference", () => {
  const value = response({ evidence_produced: false });
  delete value.evidence_envelope_id;
  const model = normalizeMeshEvidenceRefreshResponse(value, { now });
  assert.equal(model.handling.completed, true);
  assert.equal(model.evidence_reference, null);
  assert.equal(model.current_evidence_established, false);
});

test("rejects authority mismatches and premature evidence references", () => {
  assert.throws(() => normalizeMeshEvidenceRefreshResponse(response({ authority_domain: "privacy" }), { now }));
  assert.throws(() => normalizeMeshEvidenceRefreshResponse(response({ status: "received" }), { now }));
  assert.throws(() => normalizeMeshEvidenceRefreshResponse(response({
    producer: {
      system: "glaze-ui",
      repository: "GoreeCloud/glaze-ui",
      revision: "b".repeat(40),
    },
    authority_domain: "presentation",
  }), { now }));
});

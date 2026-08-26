import test from "node:test";
import assert from "node:assert/strict";
import {
  fetchMeshEvidenceSubject,
  normalizeMeshEvidenceSubjectView,
} from "../reference/mesh-evidence-consumer.mjs";

const subjectView = {
  subject: { kind: "service", id: "goreecloud-drive", scope: "runtime" },
  transport: { state: "available", current_count: 2, stale_count: 1 },
  authorities: [
    {
      producer: "wardveil-security",
      authority_domain: "security",
      assertions: [
        {
          assertion: "security-status",
          latest: {
            id: "wardveil-1",
            outcome: "attention",
            summary: "Security review required.",
            fresh: true,
            observed_at: "2026-08-26T22:00:00Z",
            valid_until: "2026-08-26T23:00:00Z",
            source: "wardveil://records/1",
          },
          latest_current: {
            id: "wardveil-1",
            outcome: "attention",
            summary: "Security review required.",
            fresh: true,
            observed_at: "2026-08-26T22:00:00Z",
            valid_until: "2026-08-26T23:00:00Z",
            source: "wardveil://records/1",
          },
          history_count: 3,
        },
      ],
    },
    {
      producer: "everkeep",
      authority_domain: "recovery",
      assertions: [
        {
          assertion: "restore-verification",
          latest: {
            id: "everkeep-1",
            outcome: "pass",
            summary: "Restore verification passed.",
            fresh: true,
            observed_at: "2026-08-26T21:00:00Z",
            valid_until: "2026-08-27T01:00:00Z",
            source: "everkeep://restore-verification/1",
          },
          latest_current: {
            id: "everkeep-1",
            outcome: "pass",
            summary: "Restore verification passed.",
            fresh: true,
            observed_at: "2026-08-26T21:00:00Z",
            valid_until: "2026-08-27T01:00:00Z",
            source: "everkeep://restore-verification/1",
          },
          history_count: 1,
        },
      ],
    },
  ],
};

test("preserves independent producer authority without an overall verdict", () => {
  const model = normalizeMeshEvidenceSubjectView(subjectView);
  assert.equal(model.transport.state, "available");
  assert.equal(model.authorities.length, 2);
  assert.equal(model.authorities[0].producer, "wardveil-security");
  assert.equal(model.authorities[0].assertions[0].outcome, "attention");
  assert.equal(model.authorities[1].producer, "everkeep");
  assert.equal(model.authorities[1].assertions[0].outcome, "pass");
  assert.equal("verdict" in model, false);
  assert.equal("safe" in model, false);
  assert.equal("score" in model, false);
});

test("uses Identity read credential only as bearer authorization", async () => {
  let captured;
  const model = await fetchMeshEvidenceSubject({
    meshBaseUrl: "https://mesh.goreecloud.test",
    kind: "service",
    id: "goreecloud-drive",
    scope: "runtime",
    bearerToken: "read-credential",
    fetchImpl: async (url, init) => {
      captured = { url, init };
      return { ok: true, status: 200, async json() { return subjectView; } };
    },
  });
  assert.equal(captured.url, "https://mesh.goreecloud.test/v1/evidence/subjects/service/goreecloud-drive?scope=runtime");
  assert.equal(captured.init.headers.Authorization, "Bearer read-credential");
  assert.equal(JSON.stringify(model).includes("read-credential"), false);
  assert.equal(model.authorities.length, 2);
});

test("network failure becomes transport unavailable without domain claims", async () => {
  const model = await fetchMeshEvidenceSubject({
    meshBaseUrl: "https://mesh.goreecloud.test",
    kind: "service",
    id: "goreecloud-drive",
    bearerToken: "read-credential",
    fetchImpl: async () => { throw new Error("offline"); },
  });
  assert.equal(model.transport.state, "unavailable");
  assert.deepEqual(model.authorities, []);
});

test("rejected or malformed Mesh response becomes transport invalid", async () => {
  const rejected = await fetchMeshEvidenceSubject({
    meshBaseUrl: "https://mesh.goreecloud.test",
    kind: "service",
    id: "goreecloud-drive",
    bearerToken: "read-credential",
    fetchImpl: async () => ({ ok: false, status: 403, async json() { return { error: "insufficient scope" }; } }),
  });
  assert.equal(rejected.transport.state, "invalid");
  assert.deepEqual(rejected.authorities, []);

  const malformed = normalizeMeshEvidenceSubjectView({ transport: { state: "available" }, authorities: [{ producer: "unknown" }] });
  assert.equal(malformed.transport.state, "invalid");
  assert.deepEqual(malformed.authorities, []);
});

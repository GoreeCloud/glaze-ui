import test from "node:test";
import assert from "node:assert/strict";
import {
  buildMeshEvidenceRefreshAction,
  fetchMeshEvidenceSubject,
  normalizeMeshEvidenceSubjectView,
} from "../reference/mesh-evidence-consumer.mjs";

const subjectView = {
  subject: { kind: "service", id: "goreecloud-drive", scope: "runtime" },
  transport: { state: "current", current_count: 3, stale_count: 1, refresh_required: false },
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
    {
      producer: "goreecloud-identity",
      authority_domain: "authentication",
      assertions: [
        {
          assertion: "authentication-result",
          latest: {
            id: "identity-1",
            outcome: "verified",
            summary: "Service authentication was verified by GoreeCloud Identity.",
            fresh: true,
            observed_at: "2026-08-26T22:05:00Z",
            valid_until: "2026-08-26T22:20:00Z",
            source: "identity://evidence/authentication-result/1",
          },
          latest_current: {
            id: "identity-1",
            outcome: "verified",
            summary: "Service authentication was verified by GoreeCloud Identity.",
            fresh: true,
            observed_at: "2026-08-26T22:05:00Z",
            valid_until: "2026-08-26T22:20:00Z",
            source: "identity://evidence/authentication-result/1",
          },
          history_count: 1,
        },
      ],
    },
  ],
};

test("preserves independent producer authority without an overall verdict", () => {
  const model = normalizeMeshEvidenceSubjectView(subjectView);
  assert.equal(model.candidate, "2.0");
  assert.equal(model.stable_consumer_target, "2.0.0");
  assert.equal(model.transport.state, "current");
  assert.equal(model.transport.refresh_required, false);
  assert.equal(model.authorities.length, 3);
  assert.equal(model.authorities[0].producer, "wardveil-security");
  assert.equal(model.authorities[0].assertions[0].outcome, "attention");
  assert.equal(model.authorities[0].assertions[0].current_outcome, "attention");
  assert.equal(model.authorities[0].assertions[0].usable_as_current, true);
  assert.equal(model.authorities[1].producer, "everkeep");
  assert.equal(model.authorities[1].assertions[0].outcome, "pass");
  assert.equal(model.authorities[2].producer, "goreecloud-identity");
  assert.equal(model.authorities[2].authority_domain, "authentication");
  assert.equal(model.authorities[2].assertions[0].outcome, "verified");
  assert.equal("verdict" in model, false);
  assert.equal("safe" in model, false);
  assert.equal("score" in model, false);
});

test("rejects cross-domain producer authority escalation before presentation", () => {
  const identityClaimsSecurity = structuredClone(subjectView);
  identityClaimsSecurity.authorities[2].authority_domain = "security";
  const rejectedIdentity = normalizeMeshEvidenceSubjectView(identityClaimsSecurity);
  assert.equal(rejectedIdentity.transport.state, "invalid");
  assert.deepEqual(rejectedIdentity.authorities, []);

  const privacyClaimsAuthentication = structuredClone(subjectView);
  privacyClaimsAuthentication.authorities[0] = {
    producer: "privacy-shield",
    authority_domain: "authentication",
    assertions: subjectView.authorities[0].assertions,
  };
  const rejectedPrivacy = normalizeMeshEvidenceSubjectView(privacyClaimsAuthentication);
  assert.equal(rejectedPrivacy.transport.state, "invalid");
  assert.deepEqual(rejectedPrivacy.authorities, []);
});

test("accepts legacy available lifecycle while Mesh rolls forward", () => {
  const legacy = structuredClone(subjectView);
  legacy.transport = { state: "available", current_count: 3, stale_count: 1 };
  const model = normalizeMeshEvidenceSubjectView(legacy);
  assert.equal(model.transport.state, "current");
  assert.equal(model.transport.refresh_required, false);
});

function staleSubjectModel() {
  return normalizeMeshEvidenceSubjectView({
    subject: { kind: "service", id: "goreecloud-drive", scope: "runtime" },
    transport: { state: "stale-only", current_count: 0, stale_count: 1, refresh_required: true },
    authorities: [{
      producer: "wardveil-security",
      authority_domain: "security",
      assertions: [{
        assertion: "security-status",
        latest: {
          outcome: "protected",
          summary: "Historical status only.",
          fresh: false,
          observed_at: "2026-08-26T20:00:00Z",
          valid_until: "2026-08-26T21:00:00Z",
          source: "wardveil://records/stale",
        },
        history_count: 1,
      }],
    }],
  });
}

test("stale-only evidence remains history and requires refresh", () => {
  const model = staleSubjectModel();
  assert.equal(model.transport.state, "stale-only");
  assert.equal(model.transport.refresh_required, true);
  assert.equal(model.authorities[0].assertions[0].outcome, "protected");
  assert.equal(model.authorities[0].assertions[0].freshness, "stale");
  assert.equal(model.authorities[0].assertions[0].usable_as_current, false);
  assert.equal(model.authorities[0].assertions[0].current_outcome, null);
  assert.equal(model.authorities[0].assertions[0].latest_current, null);
});

test("empty lifecycle contains no producer claims and requires refresh", () => {
  const model = normalizeMeshEvidenceSubjectView({
    subject: { kind: "service", id: "goreecloud-drive", scope: "runtime" },
    transport: { state: "empty", current_count: 0, stale_count: 0, refresh_required: true },
    authorities: [],
  });
  assert.equal(model.transport.state, "empty");
  assert.equal(model.transport.refresh_required, true);
  assert.deepEqual(model.authorities, []);
});

test("builds a stale refresh action without minting producer truth or execution authority", () => {
  const action = buildMeshEvidenceRefreshAction(staleSubjectModel(), {
    producer: "wardveil-security",
    authorityDomain: "security",
    assertion: "security-status",
    requestedAt: "2026-08-27T18:55:00Z",
  });
  assert.equal(action.action, "request-evidence-refresh");
  assert.equal(action.coordinator, "goreecloud-mesh");
  assert.equal(action.reason, "stale");
  assert.equal(action.latest_observed_at, "2026-08-26T20:00:00Z");
  assert.equal(action.target.producer, "wardveil-security");
  assert.equal(action.target.authority_domain, "security");
  assert.equal(action.requires_mesh_coordination, true);
  assert.equal(action.producer_authority_preserved, true);
  assert.equal(action.execution_authorized, false);
  assert.equal(action.refresh_completed, false);
  assert.equal("outcome" in action, false);
  assert.equal("verdict" in action, false);
});

test("builds empty refresh actions only for explicit producer-owned domains", () => {
  const empty = normalizeMeshEvidenceSubjectView({
    subject: { kind: "service", id: "goreecloud-drive", scope: "runtime" },
    transport: { state: "empty", current_count: 0, stale_count: 0, refresh_required: true },
    authorities: [],
  });
  const privacyAction = buildMeshEvidenceRefreshAction(empty, {
    producer: "privacy-shield",
    authorityDomain: "privacy",
    assertion: "privacy-status",
    requestedAt: "2026-08-27T18:55:00Z",
  });
  assert.equal(privacyAction.reason, "empty");
  assert.equal(privacyAction.latest_observed_at, null);
  assert.equal(privacyAction.target.producer, "privacy-shield");
  assert.equal(privacyAction.execution_authorized, false);

  const identityAction = buildMeshEvidenceRefreshAction(empty, {
    producer: "goreecloud-identity",
    authorityDomain: "authentication",
    assertion: "authentication-result",
    requestedAt: "2026-08-27T18:55:00Z",
  });
  assert.equal(identityAction.target.producer, "goreecloud-identity");
  assert.equal(identityAction.target.authority_domain, "authentication");
  assert.equal(identityAction.execution_authorized, false);

  assert.throws(() => buildMeshEvidenceRefreshAction(empty, {
    producer: "privacy-shield",
    authorityDomain: "security",
    assertion: "privacy-status",
  }));
  assert.throws(() => buildMeshEvidenceRefreshAction(empty, {
    producer: "goreecloud-identity",
    authorityDomain: "security",
    assertion: "authentication-result",
  }));
  assert.throws(() => buildMeshEvidenceRefreshAction(empty, {
    producer: "goreecloud-mesh",
    authorityDomain: "coordination",
    assertion: "transport-state",
  }));
});

test("does not offer producer refresh from current or transport-failure models", () => {
  assert.throws(() => buildMeshEvidenceRefreshAction(normalizeMeshEvidenceSubjectView(subjectView), {
    producer: "wardveil-security",
    authorityDomain: "security",
    assertion: "security-status",
  }));
  assert.throws(() => buildMeshEvidenceRefreshAction({
    subject: { kind: "service", id: "goreecloud-drive", scope: "runtime" },
    transport: { state: "unavailable", refresh_required: true },
    authorities: [],
  }, {
    producer: "wardveil-security",
    authorityDomain: "security",
    assertion: "security-status",
  }));
});

test("rejects inconsistent lifecycle projections", () => {
  const inconsistent = structuredClone(subjectView);
  inconsistent.transport = { state: "stale-only", current_count: 1, stale_count: 1, refresh_required: true };
  const model = normalizeMeshEvidenceSubjectView(inconsistent);
  assert.equal(model.transport.state, "invalid");
  assert.deepEqual(model.authorities, []);
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
  assert.equal(model.authorities.length, 3);
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
  assert.equal(model.transport.refresh_required, true);
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

  const malformed = normalizeMeshEvidenceSubjectView({ transport: { state: "current", current_count: 1, stale_count: 0 }, authorities: [{ producer: "unknown" }] });
  assert.equal(malformed.transport.state, "invalid");
  assert.deepEqual(malformed.authorities, []);
});

const VERSION = "goreecloud.evidence-refresh-response.v1";
const REVISION = /^[0-9a-f]{40}$/;
const STATUSES = new Set(["received", "completed", "declined", "unavailable"]);
const PRODUCER_RULES = new Map([
  ["wardveil-security", { repository: "GoreeCloud/goreecloud-wardveil-security", domains: new Set(["security"]) }],
  ["privacy-shield", { repository: "GoreeCloud/goreecloud-privacy-shield", domains: new Set(["privacy"]) }],
  ["everkeep", { repository: "GoreeCloud/goreecloud-everkeep", domains: new Set(["resilience", "recovery", "preservation", "continuity"]) }],
  ["glaze-ui", { repository: "GoreeCloud/goreecloud-glaze-ui", domains: new Set(["presentation", "design-conformance"]) }],
]);
const TOP_LEVEL_FIELDS = new Set([
  "version", "id", "intent", "producer", "authority_domain", "subject", "assertion",
  "status", "reason_code", "responded_at", "evidence_produced", "evidence_envelope_id",
  "contains_user_content", "contains_secret_material", "authority_transferred", "execution_authorized",
]);

function timestamp(value, field) {
  const parsed = value instanceof Date ? value : new Date(value);
  if (!value || Number.isNaN(parsed.getTime())) throw new Error(`${field} must be a valid timestamp`);
  return parsed;
}

function bounded(value, field, maximum, { required = false } = {}) {
  const normalized = String(value ?? "").trim();
  if (required && !normalized) throw new Error(`${field} is required`);
  if (normalized.length > maximum) throw new Error(`${field} must be at most ${maximum} characters`);
  return normalized;
}

/**
 * Normalize a canonical Mesh evidence refresh response for Glaze UI 1.6
 * Candidate presentation. Handling completion and evidence availability are
 * presented separately from producer domain truth and evidence freshness.
 */
export function normalizeMeshEvidenceRefreshResponse(response, { now = new Date() } = {}) {
  if (!response || typeof response !== "object" || Array.isArray(response)) throw new Error("refresh response must be an object");
  for (const key of Object.keys(response)) {
    if (!TOP_LEVEL_FIELDS.has(key)) throw new Error(`unexpected refresh response field: ${key}`);
  }
  if (response.version !== VERSION) throw new Error("unsupported refresh response version");
  bounded(response.id, "response.id", 128, { required: true });

  const intent = response.intent;
  if (!intent || typeof intent !== "object" || Array.isArray(intent)) throw new Error("refresh response intent reference is required");
  if (Object.keys(intent).sort().join(",") !== "coordinator_revision,id,reason,requested_at") throw new Error("refresh response intent reference is invalid");
  bounded(intent.id, "intent.id", 128, { required: true });
  if (!REVISION.test(intent.coordinator_revision ?? "")) throw new Error("intent coordinator revision must be exact");
  if (!["stale", "empty", "manual"].includes(intent.reason)) throw new Error("invalid referenced refresh reason");
  const requestedAt = timestamp(intent.requested_at, "intent.requested_at");

  const producer = response.producer;
  if (!producer || typeof producer !== "object" || Array.isArray(producer)) throw new Error("refresh response producer is required");
  if (Object.keys(producer).sort().join(",") !== "repository,revision,system") throw new Error("refresh response producer identity is invalid");
  const rule = PRODUCER_RULES.get(producer.system);
  if (!rule || producer.repository !== rule.repository || !REVISION.test(producer.revision ?? "")) throw new Error("refresh response producer provenance is invalid");
  if (!rule.domains.has(response.authority_domain)) throw new Error("refresh response authority domain does not belong to producer");

  const subject = response.subject;
  if (!subject || typeof subject !== "object" || Array.isArray(subject)) throw new Error("refresh response subject is required");
  for (const key of Object.keys(subject)) {
    if (!["kind", "id", "scope"].includes(key)) throw new Error(`unexpected refresh response subject field: ${key}`);
  }
  bounded(subject.kind, "subject.kind", 64, { required: true });
  bounded(subject.id, "subject.id", 256, { required: true });
  bounded(subject.scope, "subject.scope", 256);
  bounded(response.assertion, "assertion", 128, { required: true });
  if (!STATUSES.has(response.status)) throw new Error("invalid refresh response status");
  const reasonCode = bounded(response.reason_code, "reason_code", 64);

  const evaluatedAt = timestamp(now, "now");
  const respondedAt = timestamp(response.responded_at, "responded_at");
  if (respondedAt.getTime() < requestedAt.getTime() || respondedAt.getTime() > evaluatedAt.getTime()) {
    throw new Error("responded_at must be between requested_at and now");
  }
  if (response.contains_user_content !== false || response.contains_secret_material !== false) throw new Error("refresh response must exclude user content and secret material");
  if (response.authority_transferred !== false || response.execution_authorized !== false) throw new Error("refresh response cannot transfer authority or authorize execution");
  if (typeof response.evidence_produced !== "boolean") throw new Error("evidence_produced must be boolean");
  const evidenceId = bounded(response.evidence_envelope_id, "evidence_envelope_id", 128);
  if (response.evidence_produced && (response.status !== "completed" || !evidenceId)) {
    throw new Error("produced evidence requires a completed response and evidence envelope id");
  }
  if (!response.evidence_produced && evidenceId) throw new Error("evidence envelope id is forbidden when evidence was not produced");

  return {
    candidate: "1.6",
    kind: "evidence-refresh-response",
    request: {
      id: intent.id,
      coordinator_revision: intent.coordinator_revision,
      reason: intent.reason,
      requested_at: requestedAt.toISOString(),
    },
    producer: {
      system: producer.system,
      repository: producer.repository,
      revision: producer.revision,
    },
    authority_domain: response.authority_domain,
    subject: structuredClone(subject),
    assertion: response.assertion,
    handling: {
      status: response.status,
      reason_code: reasonCode || null,
      responded_at: respondedAt.toISOString(),
      completed: response.status === "completed",
    },
    evidence_reference: response.evidence_produced ? {
      envelope_id: evidenceId,
      validation_required: true,
    } : null,
    current_evidence_established: false,
    producer_authority_preserved: true,
    execution_authorized: false,
    invariant: "A refresh response reports producer handling only. Even a completed response with an evidence reference does not establish current domain truth until the separate producer evidence envelope is retrieved and validated.",
  };
}

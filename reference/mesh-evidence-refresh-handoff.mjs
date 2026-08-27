import { normalizeMeshEvidenceRefreshResponse } from "./mesh-evidence-refresh-response.mjs";

const EVIDENCE_VERSION = "goreecloud.evidence-envelope.v1";
const DIGEST = /^sha256:[0-9a-f]{64}$/;
const DATA_CLASSES = new Set(["public", "operational", "derived"]);
const GLAZE_CONTRACTS = new Set([
  "CONFORMANCE.md",
  "EVIDENCE_PRESENTATION.md",
  "tokens/enforcement.json",
  "tokens/evidence-presentation.json",
]);
const PRODUCER_RULES = new Map([
  ["wardveil-security", {
    repository: "GoreeCloud/goreecloud-wardveil-security",
    contractAllowed: (value) => value.startsWith("contracts/wardveil."),
  }],
  ["privacy-shield", {
    repository: "GoreeCloud/goreecloud-privacy-shield",
    contractAllowed: (value) => value.startsWith("contracts/privacy-shield."),
  }],
  ["everkeep", {
    repository: "GoreeCloud/goreecloud-everkeep",
    contractAllowed: (value) => value.startsWith("contracts/everkeep."),
  }],
  ["glaze-ui", {
    repository: "GoreeCloud/goreecloud-glaze-ui",
    contractAllowed: (value) => GLAZE_CONTRACTS.has(value),
  }],
]);
const EVIDENCE_FIELDS = new Set([
  "version", "id", "producer", "authority_domain", "subject", "assertion", "outcome",
  "source", "observed_at", "valid_until", "data_class", "summary", "payload_digest",
  "contains_user_content", "contains_secret_material",
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

function subjectTuple(subject, field) {
  if (!subject || typeof subject !== "object" || Array.isArray(subject)) throw new Error(`${field} is required`);
  for (const key of Object.keys(subject)) {
    if (!["kind", "id", "scope"].includes(key)) throw new Error(`unexpected ${field} field: ${key}`);
  }
  return [
    bounded(subject.kind, `${field}.kind`, 64, { required: true }),
    bounded(subject.id, `${field}.id`, 256, { required: true }),
    bounded(subject.scope, `${field}.scope`, 256),
  ];
}

function sameTuple(left, right) {
  return left.length === right.length && left.every((value, index) => value === right[index]);
}

/**
 * Present a completed Mesh refresh response as current evidence only after the
 * separately supplied producer envelope is fully bound to the receipt and is
 * current at evaluation time. Producer outcome remains producer truth; Glaze
 * does not synthesize an overall verdict, score, authorization, or authority.
 */
export function normalizeMeshEvidenceRefreshHandoff(response, evidenceEnvelope, { now = new Date() } = {}) {
  const evaluatedAt = timestamp(now, "now");
  const receipt = normalizeMeshEvidenceRefreshResponse(response, { now: evaluatedAt });
  if (!receipt.handling.completed || !receipt.evidence_reference) {
    throw new Error("evidence refresh handoff requires a completed response with an evidence reference");
  }

  if (!evidenceEnvelope || typeof evidenceEnvelope !== "object" || Array.isArray(evidenceEnvelope)) throw new Error("evidence envelope must be an object");
  for (const key of Object.keys(evidenceEnvelope)) {
    if (!EVIDENCE_FIELDS.has(key)) throw new Error(`unexpected evidence envelope field: ${key}`);
  }
  if (evidenceEnvelope.version !== EVIDENCE_VERSION) throw new Error("unsupported evidence envelope version");
  const envelopeId = bounded(evidenceEnvelope.id, "evidence.id", 128, { required: true });
  if (envelopeId !== receipt.evidence_reference.envelope_id) throw new Error("evidence envelope id does not match the refresh response reference");

  const producer = evidenceEnvelope.producer;
  if (!producer || typeof producer !== "object" || Array.isArray(producer)) throw new Error("evidence producer is required");
  if (Object.keys(producer).sort().join(",") !== "contract,repository,revision,system") throw new Error("evidence producer identity is invalid");
  const rule = PRODUCER_RULES.get(producer.system);
  if (!rule || producer.repository !== rule.repository || producer.system !== receipt.producer.system || producer.repository !== receipt.producer.repository || producer.revision !== receipt.producer.revision) {
    throw new Error("evidence producer provenance does not match the refresh response");
  }
  const contract = bounded(producer.contract, "evidence producer contract", 512, { required: true });
  if (!rule.contractAllowed(contract)) throw new Error("evidence producer contract does not belong to the declared producer");

  if (evidenceEnvelope.authority_domain !== receipt.authority_domain) throw new Error("evidence authority domain does not match the refresh response");
  if (!sameTuple(subjectTuple(evidenceEnvelope.subject, "evidence.subject"), subjectTuple(receipt.subject, "response.subject"))) {
    throw new Error("evidence subject does not match the refresh response");
  }
  if (bounded(evidenceEnvelope.assertion, "evidence assertion", 128, { required: true }) !== bounded(receipt.assertion, "response assertion", 128, { required: true })) {
    throw new Error("evidence assertion does not match the refresh response");
  }

  const outcome = bounded(evidenceEnvelope.outcome, "evidence outcome", 128, { required: true });
  const source = bounded(evidenceEnvelope.source, "evidence source", 512, { required: true });
  const summary = bounded(evidenceEnvelope.summary, "evidence summary", 512);
  if (!DATA_CLASSES.has(evidenceEnvelope.data_class)) throw new Error("invalid evidence data class");
  if (evidenceEnvelope.payload_digest != null && evidenceEnvelope.payload_digest !== "" && !DIGEST.test(String(evidenceEnvelope.payload_digest))) {
    throw new Error("evidence payload_digest must use sha256:<64 lowercase hex characters>");
  }
  if (evidenceEnvelope.contains_user_content !== false || evidenceEnvelope.contains_secret_material !== false) {
    throw new Error("evidence envelope must exclude user content and secret material");
  }

  const requestedAt = timestamp(receipt.request.requested_at, "response.request.requested_at");
  const respondedAt = timestamp(receipt.handling.responded_at, "response.handling.responded_at");
  const observedAt = timestamp(evidenceEnvelope.observed_at, "evidence.observed_at");
  const validUntil = timestamp(evidenceEnvelope.valid_until, "evidence.valid_until");
  if (observedAt.getTime() < requestedAt.getTime()) throw new Error("refresh evidence observation predates the refresh request");
  if (observedAt.getTime() > respondedAt.getTime()) throw new Error("refresh response cannot reference evidence observed after the response");
  if (validUntil.getTime() <= observedAt.getTime()) throw new Error("evidence valid_until must be after observed_at");
  if (validUntil.getTime() < evaluatedAt.getTime()) throw new Error("refresh evidence is expired");

  return {
    ...receipt,
    kind: "evidence-refresh-handoff",
    evidence_reference: {
      envelope_id: envelopeId,
      validation_required: false,
      validated: true,
    },
    producer_evidence: {
      outcome,
      summary,
      source,
      observed_at: observedAt.toISOString(),
      valid_until: validUntil.toISOString(),
      data_class: evidenceEnvelope.data_class,
    },
    current_evidence_established: true,
    producer_authority_preserved: true,
    execution_authorized: false,
    invariant: "Current evidence is established only by the separately validated producer envelope. Glaze presents the producer outcome without synthesizing an overall verdict, transferring authority, or authorizing execution.",
  };
}

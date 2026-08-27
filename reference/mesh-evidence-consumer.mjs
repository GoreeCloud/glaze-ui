const AUTHORITY_SYSTEMS = new Set([
  "wardveil-security",
  "privacy-shield",
  "everkeep",
  "goreecloud-mesh",
  "glaze-ui",
]);
const MESH_LIFECYCLE_STATES = new Set(["current", "stale-only", "empty"]);
const PRODUCER_AUTHORITY_DOMAINS = new Map([
  ["wardveil-security", new Set(["security"])],
  ["privacy-shield", new Set(["privacy"])],
  ["everkeep", new Set(["resilience", "recovery", "preservation", "continuity"])],
  ["glaze-ui", new Set(["presentation", "design-conformance"])],
]);

function endpoint(meshBaseUrl, kind, id, scope = "") {
  const raw = String(meshBaseUrl ?? "").trim().replace(/\/+$/, "");
  if (!raw) throw new Error("Mesh base URL is required");
  const url = new URL(raw);
  const loopback = ["127.0.0.1", "localhost", "::1"].includes(url.hostname);
  if (url.protocol !== "https:" && !(url.protocol === "http:" && loopback)) {
    throw new Error("Mesh evidence reads require HTTPS except for loopback development");
  }
  if (!String(kind ?? "").trim() || !String(id ?? "").trim()) {
    throw new Error("evidence subject kind and id are required");
  }
  const path = `${raw}/v1/evidence/subjects/${encodeURIComponent(String(kind).trim())}/${encodeURIComponent(String(id).trim())}`;
  const query = String(scope ?? "").trim();
  return query ? `${path}?scope=${encodeURIComponent(query)}` : path;
}

function transportOnly(state, reason = "") {
  return {
    candidate: "1.6",
    stable_consumer_target: "1.5.0",
    subject: null,
    transport: {
      state,
      current_count: 0,
      stale_count: 0,
      refresh_required: true,
      reason,
    },
    authorities: [],
    invariant: "Transport state is not domain truth. Evidence lifecycle state is also not domain truth.",
  };
}

function count(value) {
  return Number.isInteger(value) && value >= 0 ? value : null;
}

function meshLifecycle(transport) {
  if (!transport || typeof transport !== "object") return null;
  const currentCount = count(transport.current_count);
  const staleCount = count(transport.stale_count);
  if (currentCount === null || staleCount === null) return null;

  let state = transport.state;
  if (state === "available") {
    state = currentCount > 0 ? "current" : staleCount > 0 ? "stale-only" : "empty";
  }
  if (!MESH_LIFECYCLE_STATES.has(state)) return null;
  if (state === "current" && currentCount === 0) return null;
  if (state === "stale-only" && (currentCount !== 0 || staleCount === 0)) return null;
  if (state === "empty" && (currentCount !== 0 || staleCount !== 0)) return null;

  const expectedRefresh = state !== "current";
  if ("refresh_required" in transport && transport.refresh_required !== expectedRefresh) return null;
  return {
    state,
    current_count: currentCount,
    stale_count: staleCount,
    refresh_required: expectedRefresh,
    reason: "",
  };
}

function freshness(envelope) {
  if (!envelope || typeof envelope !== "object") return "unknown";
  if (envelope.fresh === true) return "current";
  if (envelope.fresh === false) return "stale";
  return "unknown";
}

/**
 * Convert the authenticated Mesh subject view into a Glaze UI 1.6 Candidate
 * presentation model. Producer outcomes are preserved verbatim and authority
 * groups remain separate. This function deliberately does not emit an overall
 * verdict, safety score, protection score, compliance score, or recovery score.
 */
export function normalizeMeshEvidenceSubjectView(view) {
  if (!view || typeof view !== "object") return transportOnly("invalid", "Mesh subject view is missing");
  const lifecycle = meshLifecycle(view.transport);
  if (!lifecycle || !Array.isArray(view.authorities)) {
    return transportOnly("invalid", "Mesh subject view failed structural validation");
  }
  if (lifecycle.state === "empty" && view.authorities.length !== 0) {
    return transportOnly("invalid", "Empty Mesh evidence lifecycle contained authority records");
  }

  const authorities = [];
  for (const authority of view.authorities) {
    if (!AUTHORITY_SYSTEMS.has(authority?.producer) || !String(authority?.authority_domain ?? "").trim()) {
      return transportOnly("invalid", "Mesh authority metadata is invalid");
    }
    if (!Array.isArray(authority.assertions)) {
      return transportOnly("invalid", "Mesh assertion group is invalid");
    }
    const assertions = authority.assertions.map((item) => {
      if (!String(item?.assertion ?? "").trim() || !item?.latest || typeof item.latest !== "object") {
        throw new Error("Mesh assertion entry is invalid");
      }
      const latestCurrent = item.latest_current && typeof item.latest_current === "object" ? item.latest_current : null;
      if (lifecycle.state !== "current" && latestCurrent) {
        throw new Error("Non-current Mesh lifecycle cannot contain current evidence");
      }
      return {
        assertion: item.assertion,
        outcome: item.latest.outcome,
        summary: item.latest.summary ?? "",
        freshness: freshness(item.latest),
        usable_as_current: latestCurrent !== null && freshness(latestCurrent) === "current",
        current_outcome: latestCurrent?.outcome ?? null,
        latest_current: latestCurrent ? {
          outcome: latestCurrent.outcome,
          summary: latestCurrent.summary ?? "",
          freshness: freshness(latestCurrent),
          observed_at: latestCurrent.observed_at ?? null,
          valid_until: latestCurrent.valid_until ?? null,
          source: latestCurrent.source ?? null,
        } : null,
        observed_at: item.latest.observed_at ?? null,
        valid_until: item.latest.valid_until ?? null,
        source: item.latest.source ?? null,
        history_count: Number.isInteger(item.history_count) ? item.history_count : 0,
      };
    });
    authorities.push({
      producer: authority.producer,
      authority_domain: authority.authority_domain,
      assertions,
    });
  }

  return {
    candidate: "1.6",
    stable_consumer_target: "1.5.0",
    subject: view.subject ?? null,
    transport: lifecycle,
    authorities,
    invariant: "Producer state, authority identity, evidence lifecycle, freshness, and transport remain separate; stale history is never promoted to current domain truth and no overall domain verdict is created.",
  };
}

/**
 * Build a Glaze Candidate action descriptor for requesting refreshed producer
 * evidence through Mesh. This descriptor is presentation intent only: Glaze
 * does not mint the canonical Mesh refresh contract, contact the producer,
 * authorize execution, or claim that evidence has been refreshed.
 */
export function buildMeshEvidenceRefreshAction(model, {
  producer,
  authorityDomain,
  assertion,
  requestedAt = new Date(),
} = {}) {
  if (!model || typeof model !== "object" || !model.transport?.refresh_required) {
    throw new Error("evidence refresh action requires a refresh-required Mesh model");
  }
  if (!model.subject?.kind || !model.subject?.id) throw new Error("evidence refresh action requires a Mesh subject");
  if (!new Set(["stale-only", "empty"]).has(model.transport.state)) {
    throw new Error("producer refresh action is only available for stale-only or empty evidence lifecycle");
  }

  const targetProducer = String(producer ?? "").trim();
  const targetDomain = String(authorityDomain ?? "").trim();
  const targetAssertion = String(assertion ?? "").trim();
  if (!PRODUCER_AUTHORITY_DOMAINS.get(targetProducer)?.has(targetDomain) || !targetAssertion) {
    throw new Error("refresh target must name a known producer authority and assertion");
  }

  let latestObservedAt = null;
  if (model.transport.state === "stale-only") {
    const authority = model.authorities.find((item) => item.producer === targetProducer && item.authority_domain === targetDomain);
    const evidence = authority?.assertions?.find((item) => item.assertion === targetAssertion);
    if (!evidence || evidence.freshness !== "stale" || !evidence.observed_at) {
      throw new Error("stale refresh action must bind the selected historical producer assertion");
    }
    latestObservedAt = evidence.observed_at;
  }

  const timestamp = requestedAt instanceof Date ? requestedAt : new Date(requestedAt);
  if (Number.isNaN(timestamp.getTime())) throw new Error("requestedAt must be a valid timestamp");
  return {
    candidate: "1.6",
    action: "request-evidence-refresh",
    coordinator: "goreecloud-mesh",
    target: {
      producer: targetProducer,
      authority_domain: targetDomain,
      subject: structuredClone(model.subject),
      assertion: targetAssertion,
    },
    reason: model.transport.state === "stale-only" ? "stale" : "empty",
    requested_at: timestamp.toISOString(),
    latest_observed_at: latestObservedAt,
    requires_mesh_coordination: true,
    producer_authority_preserved: true,
    execution_authorized: false,
    refresh_completed: false,
    invariant: "This Glaze action descriptor requests coordination only; it is not producer evidence, execution authority, or proof that refresh occurred.",
  };
}

/**
 * Fetch a Mesh subject view using a GoreeCloud Identity bearer credential with
 * mesh.evidence.read scope, then convert it to the Candidate presentation model.
 * Credentials are used only in the Authorization header and never returned.
 */
export async function fetchMeshEvidenceSubject({
  meshBaseUrl,
  kind,
  id,
  scope = "",
  bearerToken,
  fetchImpl = globalThis.fetch,
  signal,
} = {}) {
  const token = String(bearerToken ?? "").trim();
  if (!token) throw new Error("GoreeCloud Identity bearer credential is required");
  if (typeof fetchImpl !== "function") throw new Error("fetch implementation is required");

  let response;
  try {
    response = await fetchImpl(endpoint(meshBaseUrl, kind, id, scope), {
      method: "GET",
      headers: {
        Authorization: `Bearer ${token}`,
        Accept: "application/json",
        "User-Agent": "glaze-ui/mesh-evidence-consumer",
      },
      signal,
    });
  } catch {
    return transportOnly("unavailable", "Mesh evidence transport is unavailable");
  }

  let payload;
  try {
    payload = await response.json();
  } catch {
    return transportOnly("invalid", `Mesh evidence response was invalid (HTTP ${response.status})`);
  }
  if (!response.ok || response.status !== 200) {
    return transportOnly("invalid", `Mesh evidence read was rejected (HTTP ${response.status})`);
  }
  try {
    return normalizeMeshEvidenceSubjectView(payload);
  } catch {
    return transportOnly("invalid", "Mesh evidence response failed Candidate validation");
  }
}

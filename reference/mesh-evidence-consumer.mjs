const AUTHORITY_SYSTEMS = new Set([
  "wardveil-security",
  "privacy-shield",
  "everkeep",
  "goreecloud-mesh",
  "glaze-ui",
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
    transport: { state, current_count: 0, stale_count: 0, reason },
    authorities: [],
    invariant: "Transport state is not domain truth.",
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
  if (view?.transport?.state !== "available" || !Array.isArray(view.authorities)) {
    return transportOnly("invalid", "Mesh subject view failed structural validation");
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
      return {
        assertion: item.assertion,
        outcome: item.latest.outcome,
        summary: item.latest.summary ?? "",
        freshness: freshness(item.latest),
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
    transport: {
      state: "available",
      current_count: Number.isInteger(view.transport.current_count) ? view.transport.current_count : 0,
      stale_count: Number.isInteger(view.transport.stale_count) ? view.transport.stale_count : 0,
      reason: "",
    },
    authorities,
    invariant: "Producer state, authority identity, freshness, and transport remain separate; no overall domain verdict is created.",
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

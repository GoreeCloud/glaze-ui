# Glaze UI V1.4 Evidence Reference Privacy Boundary

**Status:** Development / qualification infrastructure  
**Lifecycle effect:** None — this contract cannot promote Glaze UI V1.4 or make a consumer eligible for V1.4.

## Purpose

Glaze UI V1.4 performance, native-renderer parity, and accessibility qualification records retain content-addressed evidence references so an accepted observation can be bound to exact evidence bytes.

A SHA-256 digest proves which evidence bytes a record names. It does **not** make the remaining locator safe to retain. A signed URL, bearer-bearing URL, query credential, fragment credential, user-info string, or similarly secret-bearing locator could still leak reusable access material into a durable qualification packet even when the referenced bytes are immutable.

For that reason, all three V1.4 qualification evidence planes use the same credential-safe logical-locator boundary.

## Canonical evidence reference

The durable form remains:

`evidence+sha256:<64-lowercase-hex-digest>:<credential-safe-logical-locator>`

The logical locator may use bounded namespaced identifiers and slash-delimited paths. Examples include:

- `run-1`
- `review:authority`
- `reports/performance/run-1.json`
- `native/reference-scene-01.png`
- `accessibility/screen-reader:observation-1.json`

The locator grammar permits ASCII letters, digits, `.`, `_`, `+`, and `-`, with `:` for logical namespace segments and `/` for logical path segments. Each segment begins with an ASCII letter or digit.

## Credential and transport exclusion

Durable evidence references must not contain transport or credential-bearing syntax. The qualification contracts reject, among other forms:

- URL schemes such as `https://`;
- query strings (`?`);
- fragments (`#`);
- user-info/address markers (`@`);
- percent-encoded material (`%`);
- parameter or assignment delimiters such as `&` and `=`;
- backslashes; and
- whitespace.

Retrieval credentials, signed URLs, bearer material, cookies, provider tokens, temporary access grants, and equivalent secrets belong outside the retained qualification record. A runtime or reviewer may use separately authorized retrieval mechanisms to obtain evidence, but the durable packet stores only the digest plus credential-safe logical locator.

## Cross-plane consistency

The same evidence-reference grammar governs:

- performance measurement evidence and reviewer authority/review evidence;
- native-renderer reference/native scene evidence and reviewer authority/review evidence; and
- accessibility environment, preference, scenario, and human-review provenance evidence.

`scripts/validate_glaze_v1_4_evidence_reference_privacy.py` independently imports all three evaluators, checks all three schemas, accepts representative safe locators, rejects representative credential-bearing locators, and fails if any qualification plane drifts from the shared boundary.

## Non-promotion boundary

Credential-safe evidence references improve privacy and provenance hygiene only. They do not prove that the referenced evidence is genuine, current, sufficient, representative, correctly reviewed, or produced by an authorized authority. They do not establish measured production performance, native-renderer parity, assistive-technology/device qualification, human visual acceptance, downstream consumer acceptance, production approval, or Stable V1.4.

Stable V1.3 / `1.3.0` remains the consumer target until Glaze UI V1.4 independently satisfies every applicable lifecycle and acceptance gate.

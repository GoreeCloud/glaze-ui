# GLAZE UI V1.6 Acceptance

GLAZE UI V1.6 / `1.6.0` is the current Official Stable shared design-system release.

The shared qualification matrix is **24 verified / 0 unverified / 0 not applicable**, bound to frozen qualification source `c7509c79256b04b0aa67cb9dd0737d7588e0ae4a`. Final release/security acceptance is bound to protected source `a7180679ea851389e0f3004515f9a25f420e716d` and tree `9ff0bf7a5f9d64f109d99bf4b76b81bd2a162268`.

Final Stable security acceptance passed with zero unreviewed secret findings and zero selected dependency advisories/vulnerabilities. The deterministic source/runtime artifact, checksum manifest, CycloneDX SBOM, and provenance were published without rebuild under immutable tag `v1.6.0` / GitHub Release `392095913`, then read back byte-for-byte.

Authoritative Stable records are:

- `contracts/v1.6/stable-release.json`
- `acceptance/v1.6-stable.json`
- `acceptance/v1.6-stable-qualification-review.json`
- `acceptance/v1.6-final-security-acceptance.json`
- `acceptance/v1.6-publication-readback.json`
- `registry/lifecycle.json`
- `js/glaze-v1.6.0.mjs`

GLAZE UI `1.5.1` is the immediate known-good rollback baseline. Historical V1.5.1 and V1.6 Release Candidate evidence remains preserved and must not be rewritten.

No downstream GoreeCloud application becomes `1.6.0`-conformant or production-eligible automatically. Each consumer must explicitly target the current Stable release and satisfy fresh repository-local V1.6 adoption and acceptance evidence for its supported platforms and production boundary.

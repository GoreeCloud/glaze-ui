# Security Policy

Glaze UI is a design-system repository and should not contain production credentials, personal data, API keys, private keys, service tokens, or environment-specific secrets.

## Supported versions

Security and privacy fixes are applied to the current Stable Glaze UI baseline. Older Stable releases may receive a compatible fix when they remain an explicitly supported consumer target, an affected GoreeCloud application still depends on that release, and a safe maintenance patch is practical. A shared major-version number alone does not guarantee active maintenance for every historical minor release.

Support remains evidence-driven and version-specific. `STABILITY.md`, `CONSUMERS.md`, and `consumers/registry.json` define the current Stable boundary, supported older consumer targets, and recorded adoption state; the existence of a historical release does not by itself create an indefinite security-maintenance commitment.

## Reporting

Do not publish reusable secrets or sensitive GoreeCloud infrastructure details in an issue, pull request, screenshot, or reference example. If a report contains sensitive information, use an appropriate private GoreeCloud reporting channel rather than a public GitHub issue.

## Dependency boundary

The Glaze UI reference package intentionally uses no third-party runtime dependencies. Introducing a dependency requires explicit review of licensing, privacy, security, maintenance, and supply-chain impact.

## Browser and reference safety

The reference implementation must remain free of analytics, trackers, third-party fonts, remote icon delivery, advertising technology, and unnecessary remote scripts. Core examples must remain usable without network access.

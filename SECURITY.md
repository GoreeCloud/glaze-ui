# Security Policy

Glaze UI is a design-system repository and should not contain production credentials, personal data, API keys, private keys, service tokens, or environment-specific secrets.

## Supported versions

Security and privacy fixes are applied to the **current Stable Glaze UI baseline**. The current Stable release is the only supported active application target for GoreeCloud-controlled user-facing software.

Historical Stable releases may be inspected or patched only when necessary to support an immediate rollback, migration, incident response, or recovery path. Such maintenance never restores current conformance, never makes a historical release a supported production target, and never waives mandatory migration to the current Stable baseline.

`STABILITY.md`, `CONSUMERS.md`, and `consumers/registry.json` define the current Stable boundary and recorded migration state. A shared major-version number or historical release record does not create an active maintenance or production-support commitment for a superseded release.

## Reporting

Do not publish reusable secrets or sensitive GoreeCloud infrastructure details in an issue, pull request, screenshot, or reference example. If a report contains sensitive information, use an appropriate private GoreeCloud reporting channel rather than a public GitHub issue.

## Dependency boundary

The Glaze UI reference package intentionally uses no third-party runtime dependencies. Introducing a dependency requires explicit review of licensing, privacy, security, maintenance, and supply-chain impact.

## Browser and reference safety

The reference implementation must remain free of analytics, trackers, third-party fonts, remote icon delivery, advertising technology, and unnecessary remote scripts. Core examples must remain usable without network access.

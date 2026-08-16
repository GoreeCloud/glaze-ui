# Security Policy

Glaze UI is a design-system repository and should not contain production credentials, personal data, API keys, private keys, service tokens, or environment-specific secrets.

## Supported versions

Security and privacy fixes are applied to the current Glaze UI major version. Older versions may receive fixes when a GoreeCloud application still depends on them and a safe compatible patch is practical.

## Reporting

Do not publish reusable secrets or sensitive GoreeCloud infrastructure details in an issue, pull request, screenshot, or reference example. If a report contains sensitive information, use an appropriate private GoreeCloud reporting channel rather than a public GitHub issue.

## Dependency boundary

The Glaze UI reference package intentionally uses no third-party runtime dependencies. Introducing a dependency requires explicit review of licensing, privacy, security, maintenance, and supply-chain impact.

## Browser and reference safety

The reference implementation must remain free of analytics, trackers, third-party fonts, remote icon delivery, advertising technology, and unnecessary remote scripts. Core examples must remain usable without network access.

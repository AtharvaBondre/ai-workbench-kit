# Security and privacy

## Report a vulnerability privately

Use [GitHub's private vulnerability reporting](https://github.com/AtharvaBondre/ai-workbench-kit/security/advisories/new) for a suspected vulnerability in this toolkit. Do not open a public issue with credentials, private session content, account identifiers or an exploitable detail that exposes another user's data.

If the reporting form is unavailable, do not publish sensitive details. Open a minimal issue asking the maintainer to enable a private reporting channel, without the vulnerability payload or private data.

Never send real tokens to demonstrate an issue. Use a synthetic reproduction, affected version, expected behaviour and observed behaviour. Rotate any credential accidentally disclosed through the credential's issuing service.

## Scope and support

The latest published version is the supported release for fixes. This is a community-maintained project with no guaranteed response time. The toolkit does not manage or warrant provider accounts, live model availability, billing, shared-account privacy, or the security of a user's existing plugins/hooks.

Scripts preview changes by default and do not collect telemetry or upload reports. Explicit CLI execution launches a user-selected provider client and can use its credentials and allowance. A wrapper isolates routing variables; it is not a sandbox. Read the [privacy guide](skills/ai-workbench/references/privacy-and-billing.md) and [switching guide](skills/ai-workbench/references/switching.md).

## Contributor requirements

Use synthetic fixtures only. Keep keys, OAuth tokens, `.env` values, personal paths and transcripts out of this repository, screenshots and logs. Review changed runtime commands for shell injection, credential exposure, config precedence and unintended cross-account access. Do not add automatic account fallback, IAM changes, transcript cleanup or hidden Desktop database edits.

# Changelog

## 0.2.0 — 2026-11-24

### Guided onboarding

- Added a role/surface-based starting guide, full command recipes and a required/optional configuration field reference.
- Added `configure`: explained nonsecret questions for one profile, preview, explicit save, and overwrite protection.
- Added `check-config`: offline structure validation with field-specific repair guidance, no key lookup or provider calls.
- Added `launch --ask-key` for hidden, one-launch API/Foundry key entry in an interactive terminal; no secret arguments or persisted key.
- Unified the AI skill with Desktop-only and deterministic workflows; Desktop users no longer get routed through mandatory Python/CLI setup.
- Distinguished first-time setup acceptance checks from existing-session migration checks.
- Expanded synthetic tests for onboarding, cancellation, configuration validation and hidden-input boundaries.


## 0.1.0 — 2026-11-24

Initial public release.

### Included

- Offline visual guide and 11 canonical walkthroughs for beginners.
- Documentation, dependency-free scripts and a portable AI skill using the same procedures.
- Five named Claude access profiles with four authentication mechanisms.
- Preview-first terminal launch helpers, identity checks and credential references.
- Desktop switching/rollback guidance and honest compatibility boundaries.
- Reference manifests, small handoffs, context continuity checklists and original-path preservation.
- Local Claude/Codex token diagnostics and optimisation guidance.
- Synthetic regression tests, automated release checks, issue templates and community/security documentation.

### Known limits

No universal Desktop account-switch API or native cross-app session importer. No transfer of hidden model state. Subscription labels use the normal OAuth store rather than simultaneous isolated logins. Local usage reports are partial diagnostics, not invoices. Live provider compatibility and account entitlements must be verified in the recipient's environment. Windows uses the manual documentation path.

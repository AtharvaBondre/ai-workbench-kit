---
name: ai-workbench
description: Use when setting up Claude or Codex, switching Claude access providers or subscription accounts, preserving local coding work across apps, or reviewing local token usage with AI Workbench Kit.
---

# AI Workbench

This package offers four workflows using one local deterministic helper. Resolve paths relative to **this SKILL.md**, including when installed outside the original repository. Start with [Choose your path](references/choose-path.md): identify Claude Desktop, Codex Desktop or terminal, and new setup versus existing work. Desktop-only users do not need Python, CLI checks or profile JSON. For script workflows, use `python3 workbench.py --help` and only the relevant reference.

| User outcome | Read | First action |
|---|---|---|
| Set up Desktop or CLI | [Getting started](references/getting-started.md), then [Desktop](references/desktop.md) for GUI users | For Desktop, inspect the app; for scripts, run `doctor`. Choose only the requested route |
| Switch provider or account | [Switching](references/switching.md) and [Providers](references/providers.md) | Preview `launch` for CLI users; inspect the supported app connection controls for Desktop users |
| Continue work in another app | [Continuity](references/continuity.md) | Inventory original paths with `snapshot`; draft a small `handoff` per workstream |
| Reduce cost and inspect use | [Optimisation](references/optimisation.md) | Use `usage` on explicitly selected local files; reconcile provider billing separately |

For script profiles, use [configuration fields](references/configuration.md) and [complete recipes](references/recipes.md). `configure` creates one reviewed profile; `check-config` validates structure offline. Neither proves authentication. Explain required identifiers and optional defaults before asking for values. Secret entry belongs in the user-operated hidden terminal prompt (`--ask-key`) or secret store, never chat.

Command syntax and failure states: [Script reference](references/scripts.md). Privacy/account questions: [Privacy and billing](references/privacy-and-billing.md). Version-sensitive facts: [Compatibility and sources](references/sources.md).

## Execution contract

- Match the requested surface. A terminal wrapper does **not** change Desktop. Subscription labels share the normal OAuth credential store; they do not isolate two simultaneous logins.
- Inspect the installed version and current official documentation before provider changes. Do not guess model IDs, prices, plan entitlements, context windows or internal database schemas.
- Preserve existing provider profiles, original working paths, transcripts, rules and memories. Do not copy whole stores, install VMs, mutate app session databases, re-anchor missing paths, reset, compact or broadcast migration notices automatically.
- A manifest proves recorded bytes, not preserved model state or successful resumption. Use the acceptance checks in the continuity guide before declaring completion. Report missing sources and unverified sessions explicitly.
- Preview commands before applying. The user must authorise live account/provider changes; existing authorisation is sufficient. CLI execution requires idle confirmation and, for cloud providers, reviewed account guardrails. Never repair account mismatches by guessing another account.
- Credentials stay in the user's secret store. Reports and handoffs stay local. Shared logins and disabled remote control do not establish an absolute privacy boundary; inference still reaches the selected provider.
- Installation copies only this small self-contained package. It does not enable plugins, hooks, MCPs or alter billing. Do not install a second copy where this skill already exists.

Close out with the app, route, verified account/organisation, session continuity evidence, costs/limits checked, files changed and remaining checks. Never equate a record count with “100% seamless.”

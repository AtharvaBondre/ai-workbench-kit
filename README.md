# AI Workbench Kit

[![CI](https://github.com/AtharvaBondre/ai-workbench-kit/actions/workflows/ci.yml/badge.svg)](https://github.com/AtharvaBondre/ai-workbench-kit/actions/workflows/ci.yml)
[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)
[![Python 3.11+](https://img.shields.io/badge/Python-3.11%2B-blue.svg)](https://www.python.org/downloads/)

**Set up Claude and Codex, switch Claude access routes, and keep local work organised—with a guide, ordinary scripts, or an AI assistant.**

Read the **[online visual guide](https://atharvabondre.github.io/ai-workbench-kit/)** or download the **[latest release](https://github.com/AtharvaBondre/ai-workbench-kit/releases/latest)**. After extracting the ZIP, open **[START-HERE.html](START-HERE.html)** for the same guide offline. It works offline, uses no external fonts or analytics, and needs no account. This is a portable starter kit, version **0.1.0**, prepared on **24 November 2026**.

## Choose how you want to use it

| Option | Best for | Start here |
|---|---|---|
| **Documentation** | “Explain it and let me click through Desktop.” | [Beginner walkthrough](skills/ai-workbench/references/getting-started.md) → [Desktop setup](skills/ai-workbench/references/desktop.md) |
| **Non-AI scripts** | “Give me repeatable checks that do not spend AI tokens.” | `python3 workbench.py doctor` → [Script guide](skills/ai-workbench/references/scripts.md) |
| **AI skill** | “Let my assistant guide or operate the setup.” | [Install and use the skill](skills/ai-workbench/references/ai-skill.md) |

All three options follow the **same procedures and use the same code**. You can mix them. The AI option consumes your assistant's normal allowance; the scripts themselves do not call a model. An explicitly launched Claude CLI uses whichever provider you select.

## What is included

- Claude Desktop and Claude Code installation, first-run checks and model selection guidance.
- Five named Claude access profiles: **AWS Bedrock, Azure Foundry, Anthropic API, subscription account A and subscription account B**. Historical “Pro”/“Ultra” names are editable labels; current availability and billing must be checked with the provider.
- Process-scoped CLI launchers with preview, identity checks and credential references. No shell startup-file edits.
- A Desktop switching and rollback checklist. **A CLI wrapper does not switch the Desktop app.**
- Codex setup guidance and a read-only configuration review.
- Session file manifests and small handoff templates that reference original files. No bulk transcript or repository copying.
- Local token reports, cache diagnostics, billing checks, model/effort guidance and scoped plugin decisions.
- A portable `ai-workbench` skill covering setup, switching, continuity and usage review.

## Quick start: no AI required

**No terminal needed:** open the online guide above, or download the release ZIP, extract it, and double-click `START-HERE.html`. On GitHub, clicking an HTML source file shows its code; use the online guide to read it visually.

**Script users:** install Python **3.11 or newer** from [python.org](https://www.python.org/downloads/) if needed. Download and extract the latest release. On macOS, open Terminal, type `cd ` (including the space), drag the extracted `ai-workbench-kit` folder into the window, and press Return. Then run:

```bash
python3 workbench.py doctor
python3 workbench.py --help
```

`doctor` is offline and changes nothing. For Desktop-only use, skip Python and follow the visual guide. There is no need to install a standalone CLI just to read this kit or use Desktop.

For users who already have Git:

```bash
git clone https://github.com/AtharvaBondre/ai-workbench-kit.git
cd ai-workbench-kit
python3 workbench.py doctor
```

To install the AI option, follow the [skill guide](skills/ai-workbench/references/ai-skill.md). No provider credentials are needed to read the documentation or run the offline checks.

## Find the right guide

| I want to… | Read |
|---|---|
| Set up for the first time | [Getting started](skills/ai-workbench/references/getting-started.md) |
| Use the Desktop UI | [Desktop walkthrough](skills/ai-workbench/references/desktop.md) |
| Understand the five access profiles | [Providers and billing routes](skills/ai-workbench/references/providers.md) |
| Switch and keep a rollback path | [Switching](skills/ai-workbench/references/switching.md) |
| Continue existing work in another client | [Continuity and handoffs](skills/ai-workbench/references/continuity.md) |
| Spend less and measure usage | [Optimisation](skills/ai-workbench/references/optimisation.md) |
| Run a particular command | [Script reference](skills/ai-workbench/references/scripts.md) |
| Protect private work | [Privacy and billing](skills/ai-workbench/references/privacy-and-billing.md) |
| Investigate a failure | [Troubleshooting](skills/ai-workbench/references/troubleshooting.md) |
| Check support and current official sources | [Compatibility](skills/ai-workbench/references/sources.md) |

## Support status

This is an early, independently maintained release. The CLI helpers have synthetic regression tests; live account changes require recipient-side checks. macOS is locally tested, Linux is covered by the CI test matrix, and Windows currently has the documentation path. A successful CI run is not proof of any provider's live availability.

## Clear boundaries

This kit is independent of Anthropic, OpenAI, AWS and Microsoft. It does not provide model access, subscriptions or credits. It does not promise identical answers, transfer hidden model state, or guarantee privacy on a shared login. Preserving source files and validating a resumed workflow are separate checks.

No automatic app upgrades, logouts, transcript edits, compaction, cleanup, VM installation, API probes, billing changes, public uploads or new cloud resources. The scripts do not implement a private Desktop database importer. Read [compatibility and sources](skills/ai-workbench/references/sources.md) before applying version-sensitive settings.

## Project map

```text
START-HERE.html                    visual entry point
workbench.py                       convenient command entry point
skills/ai-workbench/SKILL.md        AI entry point
skills/ai-workbench/references/     all user guides, one canonical copy
skills/ai-workbench/scripts/        dependency-free Python implementation
skills/ai-workbench/assets/         example profiles and handoff/checklist templates
tests/                             synthetic tests; no real account calls
validation/                        test evidence and release limitations
```

See [CONTRIBUTING.md](CONTRIBUTING.md) for maintenance and testing. Reports, keys and personal profiles belong **outside this distributable folder**. Share the supplied clean ZIP, not your application data directories.

MIT licensed. See [LICENSE](LICENSE).

## Community and releases

- [Report a reproducible, redacted bug](https://github.com/AtharvaBondre/ai-workbench-kit/issues/new/choose) or [suggest an improvement](https://github.com/AtharvaBondre/ai-workbench-kit/issues/new/choose).
- Read [SUPPORT.md](SUPPORT.md), [SECURITY.md](SECURITY.md), [CONTRIBUTING.md](CONTRIBUTING.md) and [CODE_OF_CONDUCT.md](CODE_OF_CONDUCT.md) before sharing logs or contributing.
- See [CHANGELOG.md](CHANGELOG.md) for changes and [ROADMAP.md](ROADMAP.md) for considered next steps.
- Maintained by [AtharvaBondre](https://github.com/AtharvaBondre). This is a personal open-source project, independent of the model providers.

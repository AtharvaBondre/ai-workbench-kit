# Choose your path

You do not need to understand every provider or install every tool. Choose the experience you want, then follow just that path.

| You | Start with | What you need | You are finished when |
|---|---|---|---|
| Completely new; want Claude Desktop | Path A below | Claude Desktop and authorised access | Local Code opens the correct folder and a small test succeeds |
| Completely new; want Codex Desktop | Path B below | Codex Desktop and authorised access | Correct account, project and a small test verified |
| Want visuals and documentation only | Path A or B; use this online/offline guide | A browser; no Python or AI needed to read | You complete the app's supported setup checks |
| Technical, but unfamiliar with setup | Path C | Python 3.11+; the relevant CLI only | Profile check and preview pass, then authorised live access verified |
| Want scripts with no AI | Path C | Same as above; no AI needed for helper commands | Deterministic checks complete without model calls |
| Already have an AI assistant | Path D | A client supporting skills, or the manual prompt fallback | Assistant follows the same relevant guide and checks results |

## Path A — Claude Desktop, no terminal

1. Install **only Claude Desktop** from [the official download](https://claude.ai/download), or open the existing installation.
2. Sign in with the intended account and choose the intended organisation. If you need an API, Bedrock or Foundry connection, read the supported third-party section of the [Desktop guide](desktop.md); availability depends on your app build.
3. Select **Code**, then the **local computer** environment, and select your project folder. For new work, create an ordinary empty folder. For existing work, retain its original folder.
4. Check the account, route and model. Try one small, non-sensitive task; this consumes your account's normal usage.
5. If you already had sessions, verify one existing session and its pending work. If this is your first setup, skip the old-session checks.

**You do not need Python, the standalone Claude CLI, profile JSON, AWS CLI or Azure CLI for an ordinary subscription-based Desktop setup.** If the app does not offer the desired provider control, do not install extra components hoping to make it appear.

## Path B — Codex Desktop, no terminal

1. Install/open Codex using [OpenAI's official guide](https://developers.openai.com/codex/app/).
2. Sign in through the app's supported flow and verify the account and billing route.
3. Select the original project folder, or create a folder for genuinely new work.
4. Select an available routine coding model and appropriate effort. Keep normal permission prompts.
5. Run one small test. Existing users also check the original session and pending work.

**You do not need the Claude profile wizard for Codex.** This kit's Codex script reads settings and usage; it does not configure Codex as a Claude provider.

## Path C — Scripts and manual setup, no AI needed

1. Download and extract the [latest release](https://github.com/AtharvaBondre/ai-workbench-kit/releases/latest). Install Python 3.11+ if needed. Open Terminal **inside the extracted folder**.
2. Run `python3 workbench.py doctor`. This checks prerequisites offline. A missing optional AWS/Azure/Claude CLI is not a problem if you do not use that route; Desktop apps are not detected by this command.
3. For a **Claude terminal profile**, run `python3 workbench.py configure`. Answer only the selected route's questions. Use the [configuration reference](configuration.md) whenever a value is unfamiliar. The wizard previews the result and saves only if you type `save`.
4. Run `check-config` using the command shown by the wizard. This checks structure only, without looking up keys or contacting a provider.
5. Preview `launch`, then explicitly execute it only when you are ready for live Claude usage. Follow the [complete API example](recipes.md) or [script reference](scripts.md).

The helper commands themselves do not need AI. An actual Claude/Codex conversation always needs authorised model access. No helper installs a model, pays for a plan or configures Desktop invisibly.

## Path D — Let an AI assistant guide you

Install the [portable skill](ai-skill.md), or paste this request into an assistant with access to the extracted folder:

> Read `skills/ai-workbench/SKILL.md` from AI Workbench Kit. First identify whether I want Claude Desktop, Codex Desktop or a terminal workflow. Follow only that path. Explain unfamiliar fields before asking for values. Do not ask me to paste secrets into chat. Keep existing sessions and folders unchanged, preview changes, and distinguish completed checks from unverified access.

If the assistant cannot read local files or operate apps, it can explain the steps, but you perform them manually. Skill discovery and computer-control capabilities differ by client. Do not pretend a skill is active simply because a file was downloaded.

## Stuck at a step?

Use [configuration](configuration.md) for values and key references, [recipes](recipes.md) for complete command sequences, and [troubleshooting](troubleshooting.md) for failure symptoms. Stay on the current step until the stated result is visible; no need to complete every route.

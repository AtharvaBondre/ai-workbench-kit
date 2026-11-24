# Start here: your first setup

You need three things: an app, an authorised way to access a model, and a folder for your work. A model runs at the provider; it is not something you download to your laptop for this setup.

New here? Start with [Choose your path](choose-path.md). Desktop users can skip Python, terminal wrappers and JSON configuration.

## 1. Choose the experience

- **Claude Desktop, Code tab:** graphical local coding sessions. Choose the local computer environment when you want files and tools on your machine. This is the primary path for people who do not want a terminal.
- **Claude Code CLI:** optional terminal interface. Useful for repeatable wrappers, servers and scripts. Desktop may manage its own runtime; its version need not equal a separately installed CLI's version.
- **Codex desktop app:** another graphical coding assistant. Its account, provider and billing are separate from Claude's.

Chat, local Code, remote Code and Cowork can have different storage and execution behaviour. Selecting a subscription does not automatically make every surface local.

## 2. Get the apps from the official source

Install **only what your chosen path needs**:

| Your path | Install/open | Skip unless separately needed |
|---|---|---|
| Claude Desktop | [Claude Desktop](https://claude.ai/download) | Python, standalone Claude CLI, AWS/Azure CLI |
| Codex Desktop | [Codex app](https://developers.openai.com/codex/app/) | Claude profile wizard and Claude CLI |
| Non-AI helper scripts | [Python 3.11+](https://www.python.org/downloads/) | No pip packages needed |
| Claude terminal wrappers | Python plus [Claude Code CLI](https://code.claude.com/docs/en/setup) | Desktop is optional for this path |
| Bedrock/Foundry terminal routes | Their required approved CLI/auth prerequisites | Other providers' tools |

Do not install all providers, VMs, Docker, databases, MCP servers or plugins “just in case.” For an existing installation, inventory it before installing another copy. A separately installed CLI may be unnecessary for a Desktop-only workflow.

## 3. Choose who supplies and bills the model

| You have | Choose | Who records consumption |
|---|---|---|
| A Claude subscription | Subscription account | The subscription account and any enabled extra usage |
| Anthropic Console API credits/key | Direct Anthropic API | Anthropic Console organisation/workspace |
| AWS Bedrock permission | Bedrock | The selected AWS account |
| An Azure Foundry Claude deployment | Foundry | The selected Azure resource/subscription |

Two subscription accounts can be saved as named **intent profiles**, but a name does not log you in or isolate two OAuth accounts. Verify the email and organisation after every account change. See [providers](providers.md).

## 4. Create one local project

If this is new work, create an ordinary folder such as `Documents/MyCodingProject`. If you already have work, use **the original folder**. Do not create a second repository or move an old worktree just to switch the model provider.

In Desktop, select Code → local computer → that folder, using the controls available in your version. Review directory access permissions. Keep normal permission prompts; “bypass permissions” is not a setup optimisation.

## 5. Verify with a small, non-sensitive task

After checking the signed-in account, route and model, create a disposable test session in a test folder. Ask it to describe an empty example file or answer a brief question. This uses tokens. Check the response and the matching provider usage surface. If you already have work sessions, then open one, verify its folder and history, and ask it to state the current goal and next unfinished action before authorising new edits. A first-time user with no old work can skip this step.

Success in a new session alone does not prove that every old session resumed correctly.

## 6. Set economical new-session defaults

Select a currently available everyday coding model and medium effort. Choose the most capable model deliberately for difficult work. Leave paid speed boosts off unless needed. Use the model picker manually; distinguish automatic model routing from permission “Auto” modes. Preserve existing long-session choices until their context requirements are understood.

See [optimisation](optimisation.md) for cache, memory, tools and usage reviews, and [Desktop](desktop.md) for a printable checklist.

## Words you will see

- **Provider:** the service processing the model request.
- **Profile/wrapper:** a saved route and an isolated launch instruction; not a subscription purchase.
- **Organisation/workspace:** a billing/access boundary inside a provider account.
- **Context:** what a model can consider on a request; saved history can be longer than that.
- **Memory/rules:** saved instructions or facts loaded from files or an app store.
- **Prompt cache:** reuse of eligible repeated input to reduce cost/latency, not extra context capacity.
- **Handoff:** a compact description of the work plus references to its original evidence.

Next: [Desktop walkthrough](desktop.md), [script walkthrough](scripts.md), or [AI-assisted walkthrough](ai-skill.md).

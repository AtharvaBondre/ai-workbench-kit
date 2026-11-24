# Use the same toolkit through an AI assistant

The bundled **ai-workbench** skill has four modes: setup, switch access, preserve/continue work, and review usage. It contains the full script, guides and examples. It needs no separate plugin or MCP server.

The assistant must first choose Desktop or terminal and human-guided or automated work. Desktop-only users do not need Python, `doctor` or profile JSON. All modes use the same [configuration reference](configuration.md), [recipes](recipes.md) and acceptance checks.

## Install only where you want it

From the project folder, preview a Claude Code installation:

```bash
python3 workbench.py install-skill --target "$HOME/.claude/skills"
```

Apply the small package copy:

```bash
python3 workbench.py install-skill --target "$HOME/.claude/skills" --apply
```

For Codex, choose a supported skill directory, such as `$HOME/.agents/skills`, and verify discovery using your installed client's documentation. Custom Claude/Codex configuration locations may use different directories. The command does not guess them. It refuses existing destinations rather than replacing another skill.

The installed copy is self-contained; its internal links stay valid after extraction. Keeping multiple runtime copies is a deliberate installation choice, not a transcript migration. Updates require comparing the old skill and replacing it through your normal reviewed process; the installer does not silently overwrite it.

## Invoke it

In a local Claude Code session, type `/ai-workbench` if it is listed in your skills menu. In Codex, use `$ai-workbench` or its skill picker if supported. If it does not appear, inspect the selected project's runtime/skill discovery settings. Follow the client's reload instructions after tasks are idle; do not reset a session to discover a skill.

Example requests:

> Use ai-workbench to set up Claude Desktop Code using my subscription. Keep it on this computer and preserve my existing projects. Inspect first; do not change accounts until the proposed target is clear.

> Use ai-workbench to switch this local Desktop setup from API to Bedrock. I have authorised the intended account. Preserve the API profile and my current sessions, then verify one resumed workflow before calling it ready.

> Use ai-workbench to continue these selected Codex sessions in Claude. Keep the original folders, create small private handoffs, and list any source history or tools that cannot be verified.

> Use ai-workbench to review seven days of local token metadata. Do not send transcripts to another service, compact sessions or install plugins. Reconcile billing separately.

## What the assistant may do

Read the relevant guide, run offline checks, inspect supported UI, prepare small handoffs, and apply the changes you authorise. It must distinguish script preview from execution and actual Desktop state from terminal state.

Installing a skill does not automatically change configuration, enforce a spending cap, make a shared account private, or cause every session to read the usage policy. Confirm it is discovered and invoked. The assistant itself consumes normal model usage, even when the local script does not.

## If skills are unavailable

An assistant that can read local files can follow the package manually. Paste:

> Read `skills/ai-workbench/SKILL.md` in the extracted kit. I want [Claude Desktop / Codex Desktop / terminal]. Use the relevant guide and explain each required configuration field. Use `check-config` for script profiles, preview before executing, and never request a secret in chat. Report exactly what was verified.

Replace the bracketed choice. If the assistant has no filesystem or computer-control access, it can guide you, but cannot perform local actions. You can always use the same documentation and scripts without AI.

## Recommended AI sequence

1. Choose the actual product/surface and new setup versus existing-work migration.
2. Read only its relevant path; do not install every provider.
3. Explain required identifiers and secret references before collecting values.
4. For scripts, create a reviewed profile, run offline validation, then preview. For Desktop, inspect supported controls instead.
5. Perform only authorised live changes and verify the account/model/session results separately.
6. Preserve the original workflow and clearly label anything still unverified.

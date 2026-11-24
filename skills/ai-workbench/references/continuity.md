# Preserve work and move context without duplicating everything

There are two different operations:

- **Change the provider in the same client:** original local files can stay where they are, while the client changes authentication/routing. Session access still needs checking after account changes.
- **Move from Codex to Claude (or back):** preserve the original histories and create a useful continuation handoff. The destination cannot inherit hidden model state, live tool handles or an identical native conversation automatically.

A concise handoff can miss detail. Keep original history references accessible and use them when needed; do not describe a summary as a lossless replacement for the source.

## What stays in place

Repositories, worktrees, files, scripts, local `.env` files, CLI installations and credential stores normally stay on the same machine. Do not copy secrets into Obsidian or handoffs. Record locations and safe verification commands, such as a named AWS profile and expected account—not the keys.

An installed CLI is not proof that the destination app inherits its PATH, login, shell functions or configuration. Check from the actual destination session. Reuse existing sign-ins when authorised; perform a fresh login if required by the tool instead of transferring token blobs.

## A small private context library

Create a separate local root of your own, outside shared/synchronised folders unless sharing is intended:

```text
My AI Continuity/
  README.md                       navigation and conventions
  Projects/
    Example project/
      index.md                    original folder and session links
      Sessions/
        session-a-handoff.json    goal, decisions, pending work, references
        session-b-handoff.json
  Verification/
    before.json                   file paths, sizes, hashes
    comparison.json
    session-checklist.csv
```

Obsidian can open this folder as a local vault. A separate folder name alone does not guarantee privacy: inspect Obsidian Sync, Git, iCloud/OneDrive and sharing settings first. No sync/upload is needed for this workflow.

## Per-session checklist

For each active **and** archived source session, record:

1. Stable source ID, title, project group, parent/child relationships, pins and archive status.
2. Exact original project/worktree path and whether it still exists.
3. Current goal, important decisions, constraints, last verified result and remaining tasks.
4. Relevant memory/rules/skills/scripts and source-history references.
5. Required CLI tools, environment variable **names**, auth **locations**, expected accounts and safe verification steps.
6. Destination entry/link, handoff-read confirmation, context check, actual folder, tool checks and unresolved gaps.

Do not silently substitute a new directory for a missing worktree. Stop that session's continuation, locate the original work and reconcile uncommitted changes first.

## Practical script sequence

Create a private output directory outside the source roots. Inventory only explicitly selected files/folders, while the app is idle:

```bash
mkdir -p "$HOME/Documents/My-AI-Continuity/Verification"
chmod 700 "$HOME/Documents/My-AI-Continuity"
python3 workbench.py snapshot \
  "$HOME/Documents/MyCodingProject/handoff.md" \
  --output "$HOME/Documents/My-AI-Continuity/Verification/before.json"
```

Use a real existing source path. For session preservation, explicitly select the relevant original transcript files too; default locations and formats depend on the client. This script does not automatically discover all app histories.

```bash
python3 workbench.py handoff \
  --title "Continue example project" \
  --project "$HOME/Documents/MyCodingProject" \
  --sources "$HOME/Documents/MyCodingProject/handoff.md" \
  --output "$HOME/Documents/My-AI-Continuity/example-handoff.json"
```

Fill the handoff's context fields using actual source evidence. The script creates a skeleton and references; it does not infer decisions or transfer a native conversation.

In Claude Desktop's local Code surface, select the original folder and create a continuation. Ask it to read that handoff and only the relevant references. First ask it to state the objective, last result, constraints and next action. Reconcile discrepancies before edits. The AI will process the content you ask it to read through the selected provider.

Afterwards:

```bash
python3 workbench.py compare \
  "$HOME/Documents/My-AI-Continuity/Verification/before.json" \
  --output "$HOME/Documents/My-AI-Continuity/Verification/after.json"
```

`unchanged`/`appended` are file observations, not proof of complete context. Appending history may be expected; changed/missing original files require investigation. The manifest contains hashes and paths only and **cannot restore a deleted file**. Keep a normal independent backup if recovery from disk failure is required.

## Grouping and visibility

Match group names, nesting and pins through supported destination UI controls. Cross-app hierarchy may not have an exact equivalent; retain the full source relationship in the index. Check Code versus Chat, local versus remote, collapsed groups, archived filters, Show more and search before concluding a session disappeared.

Counts are a useful reconciliation check, but every required session needs a source-to-destination row. A record that exists on disk may still be invisible or unusable in the app.

## What not to do

- No whole-store duplicate copies for a context handoff.
- No direct edits of private Desktop SQLite/JSON session stores.
- No automated deletion, compaction, reset, cleanup, “repair” re-anchoring or force restart.
- No mass messages to old sessions as a migration marker: those messages may wake models, bill large histories and trigger compaction.
- No promises that shared accounts expose nothing or that a different model will behave identically.

Skills should be audited by package, not just name. Preserve their scripts/references, check tool compatibility and resolve symlinks before removing old source directories. An MCP server, app connector and CLI login are different capabilities; verify each actually needed one.

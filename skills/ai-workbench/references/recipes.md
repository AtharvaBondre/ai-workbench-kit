# Complete command recipes

Use these on macOS/Linux from the extracted kit folder. No AI is needed for helper commands. An actual model conversation still needs authorised access and can consume allowance or credits.

## First: open the right folder

On macOS, open Terminal. Type `cd ` with a trailing space, drag the extracted `ai-workbench-kit` folder into the window, then press Return. On Linux, open Terminal in that folder using your file manager, or run `cd /absolute/path/to/ai-workbench-kit` with your actual path.

```bash
python3 --version
python3 workbench.py --help
```

Expected: Python 3.11+ and the kit's command list. If `workbench.py` is not found, change into the extracted folder. Do not paste the example `/absolute/path/...` unchanged. Quote paths with spaces, as the commands below do.

## A. Set up one API terminal profile without editing JSON

**Terminal launch prerequisite:** install Claude Code CLI using the [official setup instructions](https://code.claude.com/docs/en/setup). Installing the Desktop app alone is not this step. Run `doctor` below and check that `executables.claude` is `true`; if it is `false`, finish the official CLI installation and reopen Terminal before continuing to a live launch. Offline configuration and preview can work without the CLI, but execution cannot. Desktop-only users can skip this entire recipe and use the [Desktop guide](desktop.md).

```bash
python3 workbench.py doctor
python3 workbench.py configure
```

Wizard answers:

1. Choose **2 — Anthropic API**.
2. Keep label `api`, or choose your own short label.
3. Choose **1 — Environment variable NAME**.
4. Enter `WORKBENCH_ANTHROPIC_KEY` as the reference name. **Do not enter the API key here.** You can use hidden input at launch instead of preloading this variable.
5. Enter a verified API model ID, or press Return to keep the client/provider default. A default is not necessarily cheapest.
6. Review the private JSON preview and output path. Type `save` to create the file, or `cancel` to leave everything untouched.

If the default file already exists, keep it and use a new filename:

```bash
python3 workbench.py configure --output "$HOME/.config/ai-workbench/api-second.json"
```

Use that same filename in every later `--config`. Likewise, replace `api` below if you chose another profile label.

```bash
python3 workbench.py check-config --config "$HOME/.config/ai-workbench/profiles.json"
```

Expected: `valid: true` and `authentication: "not checked"`. Fix named fields first if validation fails.

Preview using your **real original project folder** in place of the example:

```bash
python3 workbench.py launch api \
  --config "$HOME/.config/ai-workbench/profiles.json" \
  --project "$HOME/Documents/MyCodingProject"
```

Expected: `mode: "preview"`, no conflicts, no login or key prompt, Desktop unchanged. If the folder is missing or a setting conflicts, stop and read the explanation. Do not create a different folder to hide a missing-work problem.

**The next command starts live terminal Claude and can consume API credits.** Run it only when existing tasks are idle and this is the route you intend:

```bash
python3 workbench.py launch api \
  --config "$HOME/.config/ai-workbench/profiles.json" \
  --project "$HOME/Documents/MyCodingProject" \
  --execute --confirm-idle --ask-key
```

Paste your key into the hidden terminal prompt, not the command or chat. Verify the model/route before sending work. This does not switch Claude Desktop. For a saved Keychain method or another provider, use the [field reference](configuration.md).

## B. Other access profiles

Use the same configure → check-config → preview → execute sequence. The wizard's choices are **1 Subscription**, **3 Bedrock**, and **4 Foundry**. Choose only a route you already have approval and access to.

Subscription profiles use native sign-in separately and verify the intended account/organisation; they do not switch logins automatically. Bedrock/Foundry execution also requires `--reviewed-provider-policy` after you read your account guardrails. Foundry `--ask-key` works only for its `key_env` route. There is no API key prompt for subscriptions or Bedrock.

## C. Review Codex without reconfiguring it

```bash
python3 workbench.py codex-review --config "$HOME/.codex/config.toml"
```

Expected: selected nonsecret configuration fields, recommendations, and `changed: false`. If the file does not exist or you use another `CODEX_HOME`, locate the actual supported configuration rather than creating a fake file. Check effective Desktop settings in the app separately.

## D. Preserve references and check existing files

Create a private destination outside the folders being inventoried:

```bash
mkdir -p "$HOME/Documents/My-AI-Continuity/Verification"
chmod 700 "$HOME/Documents/My-AI-Continuity"
```

Replace the example source with a real existing handoff or selected transcript. Do not paste your whole home directory or credential store here.

```bash
python3 workbench.py snapshot \
  "$HOME/Documents/MyCodingProject/handoff.md" \
  --output "$HOME/Documents/My-AI-Continuity/Verification/before.json"
python3 workbench.py compare \
  "$HOME/Documents/My-AI-Continuity/Verification/before.json"
```

Expected before changes: `unchanged` for the selected file and zero changed/missing files. This saves hashes and paths, not a recoverable file backup. Use the [continuity guide](continuity.md) to create a handoff and verify actual session context.

## E. Make a private usage report

Select actual non-overlapping JSONL session sources; replace the example source path:

```bash
python3 workbench.py usage /absolute/path/to/selected/session.jsonl \
  --source claude --days 7 \
  --output "$HOME/Documents/My-AI-Continuity/usage-week-01.json"
```

Use `--source codex` for supported Codex logs. Expected: a new private report, no transcript text, no model call. `partial-data` or `insufficient-data` means limitations or missing evidence, not healthy zero use. Choose a new output filename for each run; existing reports are never overwritten. Billing and full prompt/subagent costs require separate native/provider checks.

## F. Install the optional AI skill

```bash
python3 workbench.py install-skill --target "$HOME/.claude/skills"
```

Expected: `action: "preview"`, with source and destination. To copy the self-contained skill after reviewing the target:

```bash
python3 workbench.py install-skill --target "$HOME/.claude/skills" --apply
```

For Codex, use its supported skills directory, commonly `"$HOME/.agents/skills"`. Existing destinations are refused. Follow [AI skill discovery and invocation](ai-skill.md); installing a file is not evidence the client loaded it.

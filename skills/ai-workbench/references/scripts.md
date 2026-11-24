# Non-AI script reference

These scripts use Python 3.11+ standard library. Run from the extracted project folder:

```bash
python3 workbench.py --help
```

Inside an installed skill, the same `python3 workbench.py ...` commands work from its directory; `python3 scripts/workbench.py ...` also works. All entrypoints execute the same implementation. The synthetic suite passes on macOS and Ubuntu CI with Python 3.11 and 3.13; live provider compatibility still needs recipient-side verification. Windows users should use the documentation path for this release.

## Commands and side effects

| Command | Reads | Writes / external calls |
|---|---|---|
| `doctor` | Executable presence, environment variable names, disk space | None; offline |
| `init --output FILE` | Example profile template | One new 0600 file; refuses overwrite |
| `launch NAME --config FILE --project DIR` | Profile and known settings files | Preview only; no login or key lookup |
| `launch ... --execute --confirm-idle` | Credentials and identity | Identity checks; starts interactive **terminal** Claude; its subsequent work can cost money |
| `snapshot PATH... --output FILE` | Explicit original files, streamed hashes | One small manifest, no source copies |
| `compare MANIFEST [--output FILE]` | Manifest and current files | Prints comparison or creates new private report |
| `handoff --title TEXT --project DIR --sources PATH... --output FILE` | Original path references | One handoff skeleton; no native session import |
| `usage PATH... --source claude\|codex --days 7 --output FILE` | Selected JSONL usage fields | Private metadata report; no inference or upload |
| `codex-review --config FILE` | Selected TOML fields | Prints recommendations; no edits |
| `install-skill --target DIR [--apply]` | Bundled self-contained skill | Preview by default; apply copies only the small skill package, never overwrites |

`--output` requires an existing parent folder. All output files are created exclusively with owner read/write permissions on POSIX. Existing files and destination symlinks are refused. Do not put an output inside a source folder being inventoried. Reports can contain private paths/identifiers; keep them local.

Exit status: **0** successful check/action, **2** stopped safely on configuration/error, **3** a manifest comparison found changed/missing source files. Python argument errors also use 2. A launched Claude process returns its own exit status.

## Make your private profile file

```bash
mkdir -p "$HOME/.config/ai-workbench"
chmod 700 "$HOME/.config/ai-workbench"
python3 workbench.py init --output "$HOME/.config/ai-workbench/profiles.json"
```

Open that JSON file in a text editor. Fill only the profiles you intend to use; delete unused example entries if helpful. `REPLACE_...` values are intentional blockers. Use actual available model IDs/deployment names; the example does not invent them.

Credential choices for API/Foundry:

```json
{"kind":"api","key_env":"WORKBENCH_ANTHROPIC_KEY"}
```

or, on macOS:

```json
{"kind":"api","keychain_service":"ai-workbench-anthropic","keychain_account":"personal-api"}
```

These are references, **not** the credential. Add the corresponding generic password through Keychain Access or use your existing trusted secret loader. Do not put the secret in a terminal command/history. The script does not create keys or modify Keychain.

## Preview a route

```bash
python3 workbench.py launch api \
  --config "$HOME/.config/ai-workbench/profiles.json" \
  --project "$HOME/Documents/MyCodingProject"
```

A preview does not prove authentication. It lists recognised configuration conflicts by key name, never their values. Relative `CLAUDE_CONFIG_DIR` values are rejected to avoid scanning one store and launching another. The scanner checks user, local, ancestor-project and known managed JSON settings; it cannot attest to remote policy, custom hooks or every future client schema. Review those separately.

For an approved CLI launch add `--execute --confirm-idle`. Bedrock/Foundry also require `--reviewed-provider-policy` after you have read your profile/account rules. It never changes provider account defaults. `--resume` accepts an existing verified Claude CLI session identifier. No arbitrary extra flags are forwarded.

For subscription accounts, `claude auth status --json` must report `loggedIn: true`, `authMethod: "claude.ai"`, matching `email` and `orgId`. Unknown schema stops execution. Do not alter the code to force a match; consult the installed client and supported account flow.

## Weekly local report

Choose specific non-overlapping source session files, or a verified directory containing the intended JSONL sessions:

```bash
python3 workbench.py usage /absolute/path/to/selected/session.jsonl \
  --source claude --days 7 \
  --output "$HOME/.config/ai-workbench/usage-week-01.json"
```

Use `--source codex` for supported Codex event logs. The script reads no cloud Console and estimates no dollar prices. It omits message text. Invalid or incomplete usage counters are skipped and counted as `skipped_usage_records`; reports with such gaps show `partial-data` or `insufficient-data`, rather than healthy zero usage. Cache warnings, premium-model shares and large recorded-request signals are partial evidence. Full prompt/subagent costs and actual billing require the native/provider review.

Roots that are symlinks or missing are rejected. Nested symlinks are excluded; their targets are not silently traversed. A file hash manifest is not a full disk backup. Use [continuity](continuity.md) for preservation and migration limits.

## Review Codex without rewriting it

```bash
python3 workbench.py codex-review --config "$HOME/.codex/config.toml"
```

This prints selected model/provider/effort/tier fields and profile names, not secrets. Those labels can still be private. Use the correct file if `CODEX_HOME` differs. It does not rewrite provider configuration or prove the effective Desktop selection.

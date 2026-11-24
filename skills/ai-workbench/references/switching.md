# Change access without changing your work

Treat switching as three separate layers:

```text
Work layer         repository • worktree • transcript • memory • handoff
                         stays in its original location
Client layer       Desktop account/profile OR terminal child process
                         changes through supported controls
Provider layer     identity • model • permissions • billing
                         verified for the chosen route
```

## The switching sequence

1. **Choose the target.** Record Desktop or CLI, provider, account, organisation, model and billing owner. Do not guess from a browser login.
2. **Reach an idle boundary.** Let the current turn finish, save edits and capture pending work. Changing authentication while a task runs can interrupt it.
3. **Record recovery information.** Keep the previous profile and a small handoff; hash explicitly selected files if desired. A hash is not a backup. Existing independent backups remain useful, but this kit does not create bulk copies.
4. **Preview.** For CLI, run `launch` without `--execute`. For Desktop, inspect the connection/account UI and prepare only the intended change.
5. **Resolve conflicts.** Review provider keys, model defaults, settings scope, managed policy, custom hooks and proxies. The launcher stops on recognised conflicts; it does not erase them.
6. **Switch in the requested surface.** Use official Desktop controls or an explicitly executed terminal wrapper. Do not claim a CLI action changed Desktop.
7. **Verify identity and access.** Confirm account/organisation/region/resource, a harmless model response, and the billing route. Provider identity checks alone cannot prove model permissions.
8. **Verify continuity.** Open an old session in the original folder. Check its recent history, constraints, pending work, tool identities and memory references. For a migration, reconcile the full per-session inventory.
9. **Close out honestly.** List what passed and what remains unverified. Stop on missing data or wrong identity.

## CLI example: preview first

Create a private profile file following [scripts](scripts.md). From the kit folder:

```bash
python3 workbench.py launch api \
  --config "$HOME/.config/ai-workbench/profiles.json" \
  --project "$HOME/Documents/MyCodingProject"
```

After reviewing the preview and confirming that no task is running:

```bash
python3 workbench.py launch api \
  --config "$HOME/.config/ai-workbench/profiles.json" \
  --project "$HOME/Documents/MyCodingProject" \
  --execute --confirm-idle
```

For Bedrock/Foundry, also read your provider guardrails and use `--reviewed-provider-policy`. This flag records your acknowledgement; it is not evidence of IAM approval. Identity checks still run. To resume an existing CLI session, supply its verified identifier via `--resume SESSION_ID`. Do not guess an ID from a Desktop record or expect a Codex ID to be a Claude ID.

No `--desktop`, cloud execution, fork, fallback-model, remote-control or permission-bypass flags are forwarded by this helper. Desktop resumption uses the supported app interface.

## What the wrapper isolates—and what it does not

The child receives only the selected provider routing variables. The parent shell is unchanged. Existing `CLAUDE_CONFIG_DIR` is retained to avoid silently switching session stores. Conflicting provider/model settings cause a stop.

This is **routing isolation**, not a sandbox. Filesystem access, non-routing environment variables, hooks, MCPs, managed policies and OS credential stores retain their own behaviour. Remote managed settings or custom extensions can introduce settings the scanner cannot see. Review those with your administrator. Do not use the wrapper as a security boundary.

The two subscription profiles verify intent against one normal login store. They do not keep simultaneous isolated OAuth sessions. Native account sign-in remains a separate deliberate step.

## Rollback

Keep the prior route configured. If verification fails, stop new requests, finish/stop the current task safely and switch through the same supported controls back to the previous profile. Confirm its identity and session visibility again. Never restore a stale whole application directory over new work. Compare files and handoffs before selectively restoring a configuration backup.

Account restrictions, credit exhaustion and missing deployment access are provider-side issues. Switching is only useful when the alternative route is authorised and usable.

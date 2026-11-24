# Claude Desktop and Codex: the graphical path

This guide changes the **app you actually use**, not just a terminal wrapper. Control names vary by version. Inspect the current screen and official help; do not edit undocumented database files to force a screen to match these instructions.

New installation? Follow “Start a local Code session” and the account/model checks below. Old-session, previous-profile, grouping and rollback checks apply only if you already have that state.

## Before changing an existing installation

1. Record the app version, selected account/organisation, current provider and original project folders.
2. Wait until active tasks finish. Save unsaved editor changes. Do not force-quit an active task.
3. Record one or two representative session titles, current goals, pending actions and selected models. For a large migration, inventory every session separately.
4. Save a small handoff and optional hash manifest. Keep existing provider configuration available for rollback. Never include secret values in exports or screenshots.
5. Check free disk space and any automatic cleanup setting before a relaunch. A login/profile change may have different preferences.

## Start a local Code session

1. Open Claude Desktop and select its **Code** surface, commonly marked `</>`.
2. Choose the **local computer** environment, rather than a cloud execution environment.
3. Select the original project folder. Verify it exists and is the intended repository/worktree.
4. Check the account menu, organisation, connection/provider and model picker.
5. Keep normal approval permissions. Permission “Auto” controls and model-routing controls are different features.

Chat may remain visible because Desktop includes more than Code. Its presence does not mean local Code work was uploaded to Chat. There may be no supported control to hide Chat, other organisations, paid-only models or older-model submenus. Do not remove account memberships or modify app internals for cosmetic cleanup.

## Switch the actual Desktop connection

**Subscription → subscription:** after tasks are idle, use the native account switch/sign-in flow. Choose the intended email and organisation. Verify billing and plan access. Recheck local Code history in the new namespace. Sign-in in Safari does not by itself prove Desktop changed accounts.

**Third-party provider → subscription:** save the current third-party configuration using the app's supported profile/export feature, if present. Switch out of third-party mode using its supported control, then complete native sign-in. Exports may contain secrets; keep them private and inspect before sharing.

**Subscription/API → Bedrock/Foundry/API:** some editions/builds expose a third-party inference or connection page; others do not. If the control is absent, stop and use the documented supported client for that provider. Do not assume every consumer Desktop build accepts arbitrary API endpoints.

When a supported third-party configuration page exists:

1. Select or create a clearly named provider profile; preserve existing ones.
2. Enter the correct credential **source**, account/region/resource and exact model identifiers from [providers](providers.md).
3. Use the built-in connection check if appropriate. It can make a billable request.
4. Apply only after tasks are idle. Quit and reopen normally only when the UI requires it.
5. Verify the connection displayed in **Desktop**, then test a small disposable session.
6. Resume a representative old session and check folder, history, pending work and tool access.

Do not route subscription OAuth through a custom API gateway. Do not let one provider's model aliases leak into another profile.

## Model picker: reduce confusion without losing capability

- Choose the current general coding model for new work; raise capability/effort deliberately.
- A primary list plus “More models” usually separates recent/recommended and older choices; it is not evidence of two providers.
- Disable automatic model fallback/routing where the client provides that choice, if stable manual selection is your preference. Verify per-session and new-session defaults separately.
- Show estimated cost if supported, understanding that cloud credits and subscriptions may not match the estimate.
- Keep separately billed modes off unless approved. “Available in the picker” does not mean “included in the plan.”
- Only hide 200K entries or prefer 1M when the current UI supports that configuration. Preserve existing long-session settings. A larger window is not a free memory migration.

## Codex Desktop

Install/sign in through [OpenAI's guide](https://developers.openai.com/codex/app/). Select the original project folder and verify the account/provider shown by the app. Set an economical available model and medium effort for **new routine work**. Use a higher effort for tasks that need it, and verify the price of any premium speed tier.

`codex-review` reads selected TOML fields; it does not prove Desktop's effective settings. Do not overwrite an existing provider definition or log out to save tokens. Match the app's actual model and usage UI with its billing source.

## Acceptance check before saying “ready”

For a first-time setup, old-session/profile checks are **not applicable**. For an existing setup or migration, they remain required.

- [ ] Correct Desktop app, Code surface, local environment, account, organisation and provider visible.
- [ ] Selected model responds under the intended billing route.
- [ ] Original project/worktree paths unchanged; missing paths explicitly listed.
- [ ] Existing session title, history, goal and pending action inspected.
- [ ] Grouping/pins/nesting/archived visibility compared separately from record counts.
- [ ] Relevant tools work from the session's environment, with intended identities.
- [ ] Previous profile remains recoverable; rollback does not require deleting data.
- [ ] Any unverified sessions or features are named, rather than declaring complete parity.

For a failed switch, return through supported connection controls to the saved prior profile, then verify its sessions. Stop if history appears missing; consult [troubleshooting](troubleshooting.md) before creating replacement sessions.

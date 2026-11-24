# Spend less while keeping the work reliable

Start with visibility, model choice and input discipline. Do not install a collection of “optimiser” plugins before measuring a problem.

## A policy you can actually use

| Work | Starting point | Escalate when |
|---|---|---|
| Routine coding, tests, small fixes | Current general coding model, medium effort | Repeated errors or complex interactions justify more reasoning |
| Architecture, difficult debugging, final review | Most capable authorised model, medium/high effort | Further effort improves a specific unresolved question |
| Simple extraction, formatting, classification | Small model if verified capable | Accuracy degrades or important context is missing |
| Long-running sessions | Preserve their supported context choice | Measure replay/cache cost before changing workflow |
| Paid speed boosts / experimental premium models | Off by default | User explicitly needs the feature and accepts its price |

Use current model names from your account. Do not hard-code a historical price table. For new routine sessions, avoid forcing the largest context globally. The size label alone is not a token charge, but growing input can make replay and cache misses expensive.

“Auto” may refer to permissions, model selection or task behaviour depending on the UI. Inspect its meaning before changing it. Disabling permission prompts is not a token-saving measure.

## Prompt caching

Both clients/providers can cache eligible repeated input. There is usually no separate plugin to install. Keep model, tools and stable instructions consistent through a workstream. Avoid toggling MCPs/plugins every turn, paid keepalive prompts, proxy caches and speculative TTL changes.

Caching reduces eligible input cost/latency; it does not make the context window larger or preserve unsaved state. A cold first request or a gap beyond the cache lifetime can explain a miss. A cache ratio below **85%** is a review signal, not proof that the setup is broken.

For Claude local reports, input is `uncached + cache read + cache creation`; the hit ratio is `cache read / total input`. For Codex, cached input is already included in the input counter. Do not add it again, and do not sum lifetime cumulative snapshots.

## Instructions and memory

Keep global instructions short and routing-oriented. Roughly 150–200 lines can be a useful review trigger, not a hard correctness rule. Before restructuring, list every requirement, preserve the original content and map each rule to its new location.

Put detailed rules in project-specific files, with path scoping where the client supports it. Store current-state/handoff documents beside the work. Link to detail and load it when relevant. A link is not proof an assistant read the target. Do not automatically delete memories, rewrite all projects or compact active sessions.

Use [usage-policy.md](../assets/usage-policy.md) as a small project policy after adapting it. It is **not automatically loaded** merely because it exists in this kit. To make it apply, add its relevant short instructions to the appropriate supported project instruction file, after review; keep the full guide on demand.

## Tools, skills and plugins

| Option | Action |
|---|---|
| Native usage/context views | Use first; exact commands depend on installed version |
| Official session-report plugin, where available | Small project-scoped pilot; verify publisher and source before installing |
| This kit's local usage script | Use without AI for metadata counts and warning signals |
| Instruction-management skill | Use periodically with a preservation/diff check |
| Documentation or semantic-retrieval MCP | Add only to projects that repeatedly need it |
| Broad global memory MCP | Measure retrieval overhead and sharing policy before adopting |
| Cache keepalive or text-as-image token tricks | Avoid; they can cost money or hurt accuracy |

No external plugin is installed by this kit. Native cached input should be measured before attributing savings to a plugin. Use subagents selectively: they multiply inference and can duplicate context. A skill's presence is not evidence of automatic use, compatibility or lower cost.

## Weekly review, about ten minutes

1. Select the previous seven days and a clearly defined set of local session files. Generate a private `usage` report.
2. Read cache ratio, model mix, unusual growth and recorded entries above **2% of observed weekly tokens**.
3. Use the client's native `/usage`, `/context` or session-report capability **only if the installed client supports it**. The report script does not run these commands or change sessions.
4. Inspect subagent activity and complete user-prompt costs in the native report. This kit cannot reliably reconstruct those from every schema.
5. Compare with the provider Console using the same account, workspace, timezone and date range. Check month-to-date spend separately against the monthly cap.
6. Record one concrete change for future sessions. Preserve active work and review effects next week.

Claude reports deduplicate repeated message IDs. Codex reports compute deltas and exclude the first unproven cumulative baseline/reset. Forked histories can overlap; choose non-overlapping sources. Reports are partial diagnostic evidence, not billing statements.

## Codex-specific checks

Run `codex-review` against the intended TOML. Check the Desktop model/effort separately. Preserve provider configuration and required permissions. Avoid needless repeated broad searches, giant tool outputs, unnecessary parallel agents and all-history rereads. Keep concise durable handoffs and expand only the relevant evidence.

Do not alter or compact a session merely to improve a usage chart. Subscription allowances, API bills and Azure/AWS credits must be tracked separately.

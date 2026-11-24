# Diagnose the failed layer first

| Symptom | Check | Safe next step |
|---|---|---|
| Desktop still shows the old provider | Actual Desktop account/connection control | Apply the supported Desktop change; a shell wrapper is insufficient |
| Browser login succeeded but Desktop did not | Desktop callback/account menu | Finish native sign-in, verify the exact email/organisation |
| Old sessions seem missing | Code vs Chat, local vs cloud, account namespace, archives, collapsed groups, Show more, search | Stop and inspect original records and mappings; do not reset or create replacements blindly |
| Wrong project/random directory heading | Exact stored worktree path | Locate original directory and uncommitted work; do not silently point elsewhere |
| Wrapper stops with settings conflicts | Listed key names and file scopes | Review settings precedence; preserve old provider config before an explicitly authorised change |
| `orgId` unavailable in CLI auth status | Installed CLI version and official schema | Use supported native verification; wrapper intentionally refuses to guess |
| AWS `AccessDenied` | STS identity, model permission, Marketplace/account restriction | Ask authorised owner to resolve that specific restriction; no profile fishing or self-grants |
| Bedrock `Operation not allowed` across models | Exact account/region/error and provider incident/account notices | Investigate account/service restrictions; do not blame every model ID or local cache |
| Foundry deployment exists but requests fail | Deployment name, route, key/resource pairing, billing eligibility | Test correct endpoint with tiny authorised request; management status alone is not runtime proof |
| Selected model changes | Explicit default, alias resolution, fallback, session selection, provider availability | Pin an available model where supported; inspect model routing separately from permission Auto mode |
| Reset time appears | Is it a usage allowance or context limit? | A plan reset may restore allowance; it does not expand the context window or rebuild a lost session |
| “Resubscribe” while Pro appears | Billing renewal/cancellation/expiry and selected organisation | Inspect account billing; do not buy again without understanding it |
| Paid-only model/Fast mode visible | Plan entitlements and extra usage | Leave disabled. Hide only if UI supports it; don't remove memberships or edit app internals |
| Low disk space after account switch | App storage settings, VMs, caches, worktrees, automatic downloads | Measure first. Do not delete transcripts, rewind data or worktrees under a generic cleanup rule |
| Terminal works, Desktop tools fail | Runtime version, PATH, permissions, environment, login source | Verify from the actual destination session; do not copy all CLI config blindly |
| Estimated cost disagrees with Console | Period/timezone, pricing, cache, credits, retries, shared keys | Console is billing evidence; local token estimates are diagnostic |

## Evidence to capture

Record time, app/version, route, expected account identifier, non-sensitive error code, relevant model/deployment and whether a minimal request succeeds. Keep request IDs private if they reveal internal details. Do not include tokens, `.env` contents or whole transcripts in a public bug report.

## Storage and upgrades

Upgrade through official supported mechanisms after active tasks are idle. Save a small handoff and recheck session visibility and storage preferences after restarting normally. Desktop's bundled runtime and a standalone CLI need compatible behaviour, not necessarily identical version numbers.

Cowork/VM components are not automatically required for every local Code workflow. Confirm your actual features before removing or downloading them. The kit never performs storage cleanup or installs VMs. A scheduled cleanup can run during relaunch, so inspect it before attributing disappearing cache/rewind data to an account switch.

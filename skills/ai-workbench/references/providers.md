# Five access profiles, four authentication routes

The five profile names reproduce a useful operational pattern. There are **four kinds of authentication**, because the two subscription labels use the same mechanism.

```text
                         ┌─ AWS Bedrock ── named AWS profile ── AWS billing
Your local coding work ──┼─ Azure Foundry ─ resource + key ──── Azure billing
                         ├─ Anthropic API ─ API key ────────── Console billing
                         ├─ Subscription A ─ OAuth login ──── account A plan
                         └─ Subscription B ─ OAuth login ──── account B plan
```

The project directory stays the same. Requests still reach the chosen remote provider. Plan/model availability, account restrictions and cloud-region policies apply independently of this kit.

## Subscription A / subscription B

Use native Claude sign-in, confirm the **email and organisation**, then confirm the actual subscription on its account page. “Personal” and a team organisation may expose different access. An account-menu label is not a billing receipt. “Resubscribe” can mean a renewal/cancellation state or stale UI; inspect billing before buying anything again.

The example names `cloud-pro` and `cloud-ultra` are editable convenience labels. They neither establish that those products are sold nor grant an entitlement. The CLI wrapper verifies the currently logged-in `email` and `orgId` via `claude auth status --json`. If the CLI version omits these fields, it stops. Do not invent an organisation ID or bypass the check. Desktop has its own account UI and must be verified separately.

Changing between these two labels does not switch accounts automatically. Finish active work, use the official sign-in flow for the required account, then verify the intended local sessions are visible. Do not copy OAuth tokens between accounts or maintain “isolated” configuration directories without analysing their session-store effects.

## Direct Anthropic API

Create a key in your authorised Console organisation/workspace. Check credits, expiry, spend limits, API access and model availability there. A Claude subscription does not normally fund API usage; Console grants are not automatically recurring monthly grants.

Store the key using your operating system's secret storage. On macOS, create a **generic password** in Keychain Access with the example service/account values, or use your own and update the private profile. Never paste the key into profile JSON, documentation, chat, Git or a shell command.

For an environment credential reference, set it in an already trusted secret-loading process, not a startup file copied into shared projects. The wrapper reads it only for explicit execution and passes it to the child process; it never prints it. Processes launched by your assistant can inherit credentials, so review tools and hooks independently.

## AWS Bedrock

Prerequisites: approved AWS account, a dedicated named profile, correct region, permission to invoke the specific model/inference profile, and any required provider/Marketplace access.

Before any AWS operation, read your organisation's profile guardrails and identify the expected account and principal. This kit passes an explicit profile and region to STS and checks an exact principal ARN and account ID. Temporary role-session ARNs may change; resolve the approved identity rather than loosening the check or trying another account.

Use the exact available inference profile/model ID from that account. A catalog entry is not proof that invocation works. Cross-region inference requires the corresponding policies. A subscription failure, account restriction, validation error or service outage needs its own diagnosis; installing a newer CLI cannot fix an AWS account restriction.

The wrapper sets `CLAUDE_CODE_USE_BEDROCK=1`, `AWS_PROFILE`, `AWS_REGION` and `AWS_DEFAULT_REGION` for its child only. It removes conflicting inherited provider keys. It does not grant permissions, change the default AWS profile, enable Marketplace purchases or create resources.

## Azure Foundry

Prerequisites: the intended resource and deployment, approved subscription/tenant, an API key for that resource, and billing eligibility confirmed by the account owner. Cloud credits are not proof that a third-party model is covered.

The script's conservative route is **resource API-key authentication**. It checks the Azure CLI's currently selected subscription, tenant and user against the profile before launch, without changing defaults. That management-plane identity check does not prove the API key belongs to the resource; verify a minimal request and resource metrics separately.

The wrapper sets `CLAUDE_CODE_USE_FOUNDRY=1`, `ANTHROPIC_FOUNDRY_RESOURCE` and `ANTHROPIC_FOUNDRY_API_KEY`. Use the actual deployment name as `model`. Entra-only and custom gateway routes are manual workflows for this release: follow the official documentation and confirm the full credential chain. Do not guess endpoints or reuse an OpenAI-compatible path for an Anthropic Messages API request.

## Models are selected, not installed

Keep `model` absent to use the provider/client default, or set an exact model/deployment value verified for that route. A model ID from Bedrock cannot be assumed to work on Foundry or direct API. Context windows, effort levels, caching and speed modes can differ. Do not append `[1m]` or enable a 1M UI variant unless both the current client and that deployment support it.

All profiles and reports should be stored outside the shareable kit. Example profiles intentionally fail validation until filled in.

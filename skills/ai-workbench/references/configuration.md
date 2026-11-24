# Configuration: what each value means

**Desktop-only users usually do not need this file.** Use the [Desktop guide](desktop.md). These fields configure the kit's **terminal launch intent**, not a Desktop account or an application session store.

For scripts, the easiest route is `python3 workbench.py configure`. It asks only the selected route's questions and writes a new private file after you type `save`. Advanced users can use `init` and edit JSON instead.

## Three kinds of value

| Type | Example | How to handle it |
|---|---|---|
| Label or path you choose | `personal`, a profile filename, original project folder | Keep meaningful, unique and local |
| Identifier from an approved account | Email, organisation ID, AWS account, deployment name | Copy exactly from trusted account details; do not guess |
| Secret | API key, password, OAuth token | Never put in JSON, documentation or chat; use hidden input or an existing secret store |

Account identifiers and paths can still be private. A preview contains your nonsecret identifiers; do not publish it unredacted.

## File structure and common options

| Field / option | Required? | Meaning / where to get it |
|---|---|---|
| `version` | Yes | Keep `1`. This is the profile format version, not the kit release version |
| `profiles` | Yes | A nonempty object holding your named profiles |
| Profile name, e.g. `api` or `personal` | Yes | Your own lowercase label: letters, numbers and hyphens, at most 48 characters. It is not a model or login |
| `kind` | Yes | Exactly `subscription`, `api`, `bedrock` or `foundry` |
| `model` | Optional | Exact currently available model/inference-profile/deployment ID for this route. Omit to use the client/provider default; that default is not necessarily cheapest |
| `--config` | For checking/launching | Path to the file you created. The wizard defaults to `~/.config/ai-workbench/profiles.json` |
| `--project` | For launch/handoff | Existing original project directory. Not a copied repository or a transcript folder |
| `--resume` | Optional | Verified existing Claude CLI session identifier; a Codex ID is not interchangeable |

Names such as `cloud-pro` and `cloud-ultra` are optional labels, not special authentication methods or plan guarantees. One normal subscription OAuth store remains in use. Use separate profile files with explicit `--config` paths if that is easier; the wizard never overwrites or automatically merges an existing file.

## Subscription account

| Field | Required? | Where to find the value / common mistake |
|---|---|---|
| `email` | Yes | Email of the intended signed-in Claude account. Confirm in the actual client |
| `organization_id` | Yes | `orgId` from the intended account's supported `claude auth status --json` output. This is an ID, **not** the word `Personal` or a team display name |
| `model` | Optional | A model available to that subscription and client version |

Use native login to select the intended account first. Check the authentication status without posting its output publicly. If the installed client omits `orgId`, the wrapper cannot verify this route; use the supported native client path and current documentation rather than inventing a value. This check does not control Desktop's separate account selection.

## Direct Anthropic API

| Field | Required? | Meaning / source |
|---|---|---|
| `key_env` | Choose this **or** the Keychain pair | The **name** of a variable, such as `WORKBENCH_ANTHROPIC_KEY`. Its value would be the key in the launching process. The JSON stores only the name |
| `keychain_service` | Required with Keychain method | Existing macOS generic-password item's service/name |
| `keychain_account` | Required with Keychain method | That item's account label; this is a local lookup label, not necessarily an email |
| `model` | Optional | Exact API model ID confirmed available in the intended Anthropic Console account |

Choose exactly one credential-reference method. API credits and limits belong to the Console organisation/workspace associated with the key; a subscription account does not select that API billing pool.

## AWS Bedrock

| Field | Required? | Meaning / source |
|---|---|---|
| `aws_profile` | Yes | Approved named AWS CLI profile, from your profile configuration/account owner |
| `region` | Yes | Approved Bedrock runtime region, such as `us-west-2` only if that is your authorised deployment region |
| `account_id` | Yes | Expected 12-digit AWS account, from your account guardrails |
| `principal_arn` | Yes | Expected exact IAM/STS principal ARN, from the approved identity record. An assumed-role session ARN can change |
| `model` | Optional, often useful | Available Bedrock model or inference-profile ID, not a direct API alias assumed to work everywhere |

Before any AWS command, read your organisation's profile guardrails and verify the intended scope, account and region. The wrapper uses explicit profile/region for STS and stops on a mismatch. It does not create a profile, log in, buy access, change defaults or grant permissions. If your organisation requires a different identity pattern, ask its owner; do not weaken the check or try unrelated profiles.

## Azure Foundry

| Field | Required? | Meaning / source |
|---|---|---|
| `resource` | Yes | Foundry resource **name** from resource Overview; not its URL and not the deployment name |
| `subscription_id` | Yes | Approved Azure subscription ID from the resource/account |
| `tenant_id` | Yes | Approved directory/tenant ID |
| `azure_account` | Yes | Expected user/account name in Azure CLI's approved account details |
| `key_env` or Keychain pair | Yes, choose one method | Reference to the **resource's** API key, using the same rules as the API route |
| `model` | Optional, normally set | Exact **deployment name** within that resource |

The helper supports the resource API-key route. It compares Azure CLI's current identity with these expected values without changing defaults. A correct management-plane identity does not prove the key/resource/deployment pairing; that needs an authorised live test. Entra-only routes follow the official manual procedure in this release.

## Enter a key without shell history or JSON editing

**Simplest one-time option on macOS/Linux:** choose `key_env` in the wizard and give it a meaningful name, even if the variable does not yet exist. At the explicit live launch, add `--ask-key`:

```bash
python3 workbench.py launch api \
  --config "$HOME/.config/ai-workbench/profiles.json" \
  --project "$HOME/Documents/MyCodingProject" \
  --execute --confirm-idle --ask-key
```

Run this yourself in an interactive terminal. Paste the key only into the **hidden input prompt**, where characters do not echo, then press Return. The key is used in the child process for that launch and is not written by the kit to a file or command history. Do not append the key to the command, pipe it into the program, or paste it into an AI chat. `--ask-key` only applies to API/Foundry profiles using `key_env`, and never prompts during a preview.

**Persistent macOS option:** use Keychain Access to create a generic password item. In its current UI, map **Keychain Item Name / service** to `keychain_service`, **Account** to `keychain_account`, and put the secret only in its **Password** field. The selected Keychain must be unlocked and accessible to the launcher. This toolkit looks up an existing item; it never creates one automatically. Do not put secrets into the item name/account fields.

**Existing secret-loader option:** if your shell already receives the key through an approved secret manager, set `key_env` to that variable's name and omit `--ask-key`. The variable must be available in the process launching the kit; naming it in JSON does not populate it. Avoid shared shell startup files and plaintext `.env` copies for this setup.

In all cases the launched process and its trusted tools can access the key. This is not a sandbox or a promise that a third-party client never records sensitive data.

## Check before using

```bash
python3 workbench.py check-config --config "$HOME/.config/ai-workbench/profiles.json"
```

- `valid: true` means supported structure and required fields passed. It does **not** mean authenticated, billed correctly or model-ready.
- Missing-field and placeholder errors identify the field to fix. Use the tables above.
- Credential-like values are rejected for recognised patterns, but this is not complete secret detection. Never supply a secret to configuration fields.
- A valid profile still needs a launch preview to check recognised app-settings conflicts, then explicit live identity/access verification.

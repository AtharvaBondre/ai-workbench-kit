# Privacy, account sharing and billing

## Local work still uses remote inference

Local Code generally means execution and working files are on your computer. The model still receives prompts and relevant file/tool content through the selected provider. Retention, training, logging and data-residency policies depend on the product, account, contract and configuration. Verify current terms; do not assume a blanket zero-retention policy.

A shared login is not a strong privacy boundary. Local-only transcripts may not appear in every teammate's UI, but cloud sessions, shared projects, remote-control features, synced storage, logs and account-level access can expose information. Disabling remote control reduces one exposure path; it does not guarantee all content is private. Apply a supported managed policy only when its current schema is verified, and check the effective behaviour.

Keep reports and handoffs outside synced folders by default. Use OS file permissions and the normal screen/account locks. Never paste secrets into prompts, output files or screenshots. The kit's profile files contain references, not secret values, but account IDs, emails and local paths can still be private.

## Separate billing pools

| Route | What to check |
|---|---|
| Claude subscription | Plan entitlement, allowance/reset period and extra usage settings |
| Anthropic API | Console organisation/workspace, credit balance/expiry, usage, spend limit |
| Bedrock | AWS account, region/inference routing, Marketplace eligibility, budgets/invoices |
| Foundry | Subscription/resource, model billing terms, credit eligibility and invoices |
| Codex | Its selected OpenAI/other supported provider account and corresponding plan/API billing |

An API credit balance is not necessarily a monthly grant. A “resets on the first” label often describes a usage counter or monthly limit period, not replenishment of promotional credit. Read the exact billing screen and expiry terms.

A **$500 monthly cap** is an example policy, not a setting this kit changes. Check whether the actual limit is organisation-wide or workspace-specific and whether other keys/users share it. Provider limits may not be instantaneous hard cutoffs; monitor spend and provider semantics. A subscription user who also uses a shared API key can consume that API pool.

## Before any test request

Know the provider, account, organisation/resource, model and expected billing route. Make one tiny non-sensitive test if authorised. Identity success and deployment status alone are insufficient to establish runtime access.

Never purchase credits, enable extra usage, subscribe through Marketplace, lift a spending limit or grant IAM automatically as “setup repair.” Report the exact blocked step and the required account-owner action.

## Exporting or sharing this project

The release folder contains examples only. Put real profiles, report files, session manifests and credentials outside it. Before publishing modifications, scan for home paths, emails, tokens, account IDs, customer identifiers and transcript content. Gitignore rules prevent accidental additions only when correctly used; they are not secret detection.

The AI skill is instructions for your chosen assistant. Asking it to inspect private source content can send that content to that assistant's provider. Use the ordinary scripts for metadata-only local reporting when that is the required boundary.

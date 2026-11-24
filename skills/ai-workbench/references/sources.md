# Compatibility, sources and verification limits

Prepared **24 November 2026**. Treat this as a versioned starter kit, not a claim that every future app exposes the same settings.

## Verification matrix

| Surface | Evidence in this release | Limit |
|---|---|---|
| Python helpers | Synthetic unit and command-line tests on macOS | No live provider switch or real session mutation performed |
| Claude CLI | Installed help exposes `--model`, `--resume`, auth status `--json`, settings scopes | Runtime auth schema and entitlement must be checked on user's installed version |
| Codex configuration | Official configuration and auth pages were reachable during preparation | Desktop effective state still requires UI verification |
| Claude provider docs | Official URLs listed below; automated retrieval returned HTTP 403 during preparation | Provider examples require current documentation/installed-client validation before live use |
| Desktop third-party controls | Guided workflow based on observed supported controls; version/edition dependent | No universal Desktop profile API, internal DB importer or silent account switch shipped |
| Linux | Synthetic suite passes on Ubuntu CI with Python 3.11 and 3.13 | Live provider/account changes not tested |
| Windows | Manual documentation path | Automated CLI launch is deliberately unsupported |
| Subscriptions / models / prices | No fixed entitlement or price assumed | Confirm in the actual account, region and deployment |

The launcher is conservative: it stops on known conflicting model/provider settings and unavailable identity evidence. This can require a manual configuration review before it is useful on an existing customised installation. It does not silently override that installation.

## Official sources to check before applying

- [Claude Desktop download](https://claude.ai/download)
- [Claude Code setup](https://code.claude.com/docs/en/setup)
- [Claude Code Desktop](https://code.claude.com/docs/en/desktop)
- [Claude Code authentication](https://code.claude.com/docs/en/authentication)
- [Claude Code settings](https://code.claude.com/docs/en/settings)
- [Claude Code model configuration](https://code.claude.com/docs/en/model-config)
- [Claude Code on Bedrock](https://code.claude.com/docs/en/amazon-bedrock)
- [Claude Code on Microsoft Foundry](https://code.claude.com/docs/en/microsoft-foundry)
- [Claude Code skills](https://code.claude.com/docs/en/skills)
- [Anthropic Console](https://platform.claude.com/)
- [Anthropic support](https://support.claude.com/)
- [AWS CLI installation](https://docs.aws.amazon.com/cli/latest/userguide/getting-started-install.html)
- [Azure CLI installation](https://learn.microsoft.com/cli/azure/install-azure-cli)
- [Codex app](https://developers.openai.com/codex/app/)
- [Codex authentication](https://developers.openai.com/codex/auth/)
- [Codex configuration reference](https://developers.openai.com/codex/config-reference/)
- [Codex skills](https://developers.openai.com/codex/skills/)
- [Python downloads](https://www.python.org/downloads/)

If a URL moves, navigate from the provider's official documentation home. Do not substitute a third-party blog's schema or a copied secret-bearing configuration. Account purchase, plan names and model availability are external facts, not toolkit features.

Public CI evidence: [initial four-job matrix](https://github.com/AtharvaBondre/ai-workbench-kit/actions/runs/45319287002). Check [the latest CI runs](https://github.com/AtharvaBondre/ai-workbench-kit/actions/workflows/ci.yml) for newer commits.

# Release verification — 0.1.0

Date: 24 November 2026. Local host: macOS. The public repository also defines an Ubuntu/macOS CI matrix for Python 3.11 and 3.13; use its run results as the platform evidence. Tests use Python standard library and synthetic temporary files only.

## Passed

- **31 automated tests**: release inventory exclusions, symlink rejection, manifest drift, internal links, private-data patterns; isolated child routing; all five named profiles; mocked identity/launch orchestration; preview without key lookup; identity mismatch stops; settings conflict stops; null/unknown identity schemas; malformed/incomplete token counters; Claude message deduplication; Codex cumulative deltas; exclusive private writes; manifest append/change/missing detection; original-file preservation; portable skill installation; CLI option-like model rejection.
- Skill frontmatter validation with the skill-creator validator.
- All local Markdown reference links resolve.
- Shareability pattern scan: no personal home path, original private company/person labels, non-example emails or recognised private-key/token patterns found.
- Offline visual guide checked in a browser: navigation opens the script guide, Markdown table renders, access selector changes authentication/billing explanations, narrow layout remains readable.
- Independent skill pressure test: passes both with and without the new skill on core safety reasoning. The test did **not** establish that the earlier baseline was unsafe.
- Independent implementation review found malformed-counter, relative-config-path, nullable-identity and installed-command usability issues. Regression tests were added, fixes applied and the same reviewer verified all original reproductions were resolved.

Reproduce tests from the project root:

```bash
python3 -m unittest discover -s tests -v
python3 build_guide.py
python3 scripts/release_check.py
```

## Boundaries of the evidence

No real provider credentials were used. No billable model test, live sign-in, Desktop setting change, application-store mutation, real session import or account migration was performed for this release. This is a tested local helper and guidance kit, not a certification that all providers work in a particular account or Desktop build.

Desktop third-party support, actual CLI auth schema, model entitlement, effective managed policy, billing and session continuity require verification on the recipient's installation. Linux was not host-tested; Windows has the manual guide path. The usage adapters are partial diagnostics, not billing reconciliation or complete prompt/subagent accounting.

The pattern scan is a useful release check, not a mathematical proof that arbitrary future edits contain no secrets. Keep real profiles and reports outside the release directory.

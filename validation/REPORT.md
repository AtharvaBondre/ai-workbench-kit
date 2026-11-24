# Release verification — 0.2.0

Date: 24 November 2026. Local host: macOS. The public repository also defines an Ubuntu/macOS CI matrix for Python 3.11 and 3.13; use its run results as the platform evidence. Tests use Python standard library and synthetic temporary files only.

## Passed

The earlier v0.1 [public CI run 45319287002](https://github.com/AtharvaBondre/ai-workbench-kit/actions/runs/45319287002) passed all four combinations: Ubuntu/macOS with Python 3.11/3.13. For this revision, use the [latest commit-specific CI results](https://github.com/AtharvaBondre/ai-workbench-kit/actions/workflows/ci.yml). Local v0.2 checks below use synthetic data; provider calls are mocked.

- **48 automated tests**: release inventory exclusions, symlink rejection, manifest drift, internal links, private-data patterns; isolated child routing; all five named profiles; mocked identity/launch orchestration; preview without key lookup; identity mismatch stops; settings conflict stops; null/unknown identity schemas; malformed/incomplete token counters; Claude message deduplication; Codex cumulative deltas; exclusive private writes; manifest append/change/missing detection; original-file preservation; portable skill installation; CLI option-like model rejection; guided configuration for each route; cancellation and overwrite protection; missing/placeholder field errors; malformed schema rejection; hidden-key input and child-only credential propagation.
- Skill frontmatter validation with the skill-creator validator.
- All local Markdown reference links resolve.
- Shareability pattern scan: no personal home path, original private company/person labels, non-example emails or recognised private-key/token patterns found.
- Offline visual guide checked in a browser: the new path selector, field-reference tables and complete command recipe render and link correctly. The earlier v0.1 layout/access-selector checks remain historical evidence.
- Independent skill pressure test: passes both with and without the new skill on core safety reasoning. The test did **not** establish that the earlier baseline was unsafe.
- Independent implementation review found malformed-counter, relative-config-path, nullable-identity and installed-command usability issues. Regression tests were added, fixes applied and the same reviewer verified all original reproductions were resolved.

- Independent v0.2 novice walkthrough: actual configure → check-config with synthetic HOME, offline preview, mocked hidden-key launch, and actual pseudo-terminal hidden input all passed. The review found a missing CLI prerequisite and two ambiguous descriptions; these were corrected before packaging. Desktop-only instructions require no Python, CLI or profile JSON.

Reproduce tests from the project root:

```bash
python3 -m unittest discover -s tests -v
python3 build_guide.py
python3 scripts/release_check.py
```

## Boundaries of the evidence

No real provider credentials were used. No billable model test, live sign-in, Desktop setting change, application-store mutation, real session import or account migration was performed for this release. This is a tested local helper and guidance kit, not a certification that all providers work in a particular account or Desktop build.

Desktop third-party support, actual CLI auth schema, model entitlement, effective managed policy, billing and session continuity require verification on the recipient's installation. The synthetic suite also passed on Ubuntu CI; Windows has the manual guide path. The usage adapters are partial diagnostics, not billing reconciliation or complete prompt/subagent accounting.

The pattern scan is a useful release check, not a mathematical proof that arbitrary future edits contain no secrets. Keep real profiles and reports outside the release directory.

# Maintain the kit

Use Python 3.11+ with no third-party packages. Run `python3 -m unittest discover -s tests -v` from the repository root. Fixtures must use temporary directories and fake credentials; never run live account tests automatically.

The self-contained skill package is the canonical implementation. The root `workbench.py` only delegates to it. Keep user documentation in the skill's references so CLI, human and AI use do not drift. The installer copies the entire small package, including scripts and references.

For new features:

1. Identify a real user workflow and supported public interface.
2. Add a failing synthetic test for the behaviour and relevant safety boundary.
3. Implement and run focused checks, then the existing test suite.
4. Update docs, CLI help and compatibility evidence together.
5. Pressure-test the skill with a fresh assistant using synthetic state.
6. Inspect release files for secrets, private paths, transcripts and unwanted archives.

Do not add a hidden Desktop DB editor, bulk migration copier, silent authentication switcher, credential logger, API probe loop, usage keepalive, automatic cleanup, permission bypass or always-on daemon.

Before a new release, verify official source pages, installed CLI help and representative Desktop controls. Validate actual model/billing behaviour only with explicit test-account authorisation. Record what was and was not verified.

## Development and pull requests

Fork the personal repository, clone your fork, and create a focused branch from `main`. Explain the concrete user problem, the resulting behaviour, tests and any compatibility limits in your pull request. Keep changes small enough to review. This repository does not use a company-specific branching workflow.

```bash
python3 -m unittest discover -s tests -v
python3 build_guide.py
python3 scripts/release_check.py
```

CI runs the synthetic test suite on Ubuntu and macOS with Python 3.11 and 3.13. It also checks documentation links, embedded-guide freshness, release-manifest hashes and accidental private-data patterns. No provider keys or paid inference are required.

After any distributable file changes, regenerate the offline guide if documentation changed, then update the release manifest:

```bash
python3 build_guide.py
python3 scripts/release_check.py --update-manifest
python3 scripts/release_check.py
```

The manifest inventories distributable files, excluding itself, Git metadata, bytecode, caches and private output directories. Its role is file integrity and reproducibility, not protection against a compromised maintainer. The release checker is a best-effort privacy guard, not a complete secret detector.

## Publishing a release

Maintainers should review the exact tracked diff, run the checks, build a clean archive with `python3 scripts/release_check.py --package /absolute/path/to/release.zip`, and test the extracted archive. Tag the reviewed commit and publish that archive with release notes explaining tested platforms and remaining limits. Never upload a whole parent workspace or app data directory.

The visual guide is built from canonical Markdown and served by GitHub Pages from the repository's `main` branch. `index.html` redirects to `START-HERE.html`; `.nojekyll` keeps the static files intact. Keep generated output in sync with its sources.

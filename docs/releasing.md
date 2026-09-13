# Release procedure

1. Review changes, source attributions and the changelog. Preserve existing history and license.
2. For a public user-visible release, choose an appropriate semantic version in the plugin manifest. Do not commit a local `+codex.*` cachebuster. Do not create a tag unless publishing it is intended.
3. Run the README validation commands, then inspect `git diff` and `git diff --check`.
4. Run `python scripts/scan_public.py --staged` after staging. It checks the staged bytes and reports only paths/rule names. Review the staged file inventory as well; no scanner proves absence of every secret.
5. Test marketplace install in a temporary Codex profile if supported, without copying authentication or personal configuration into it. Set the profile only for that test process and restore the caller's environment. Verify the installed manifest and files, not just a success message.
6. Build with `python scripts/package_plugin.py`; inspect the archive inventory. The ZIP is a distributable bundle, not a promise of a universal ZIP-install command.
7. Commit, push when authorized, and wait for CI. If creating a release, tag the tested commit and attach the inspected archive. Record any UI/behavior checks that were not run.

CI runs on pull requests and pushes to main, with read-only repository permissions and pinned actions. It does not use repository secrets or execute an AI model. Keep additional release permissions out of the normal PR validation workflow.

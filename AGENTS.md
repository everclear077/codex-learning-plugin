# Repository instructions

## Purpose and scope

This is a Codex skills plugin, not a web app or an MCP service. Preserve the source of truth in `plugins/core-learning/`; `.agents/plugins/marketplace.json` points to that directory. The published plugin must remain self-contained. Do not create a second copy of the skill at repository root.

Read the affected code and nearest instructions before editing. Explain the user-visible goal, make a focused change, run relevant checks, and report results and limitations. User instructions and existing authorization take priority; do not add unnecessary approval steps.

## Behavioral invariants

- One active tutoring mode. Socratic practice waits for a real answer and hints instead of solving the active problem.
- User requests for direct answers remain valid; assisted work is never marked independent.
- Preserve first-attempt evidence, misconceptions and uncertainty. Do not fabricate learner time, confidence, scores or scheduler state.
- Keep learning records out of plugin caches and the public repository.
- Anki export is local file conversion, not FSRS scheduling, automatic import or a reminder service.
- Learning claims need evidence and limits. No universal speed or mastery guarantees.

## Development workflow

1. Identify the smallest change that satisfies the request. Keep runtime dependencies at zero for the exporter.
2. Update code, relevant references and examples together; avoid duplicating mode rules in multiple files.
3. For behavior changes, use the scenarios in `docs/behavior-evals.md`. Label manual review and actual model execution separately.
4. Run `python scripts/validate_repo.py`, `python -m unittest discover -s tests -v`, and `python scripts/scan_public.py`. Use `python scripts/scan_public.py --staged` before committing staged changes.
5. Run `python scripts/package_plugin.py` when changing packaged files. Record the actual checks; do not claim unrun cross-platform checks passed.

Use Python 3.10-compatible syntax, UTF-8 and LF. Use pathlib, explicit encodings, clear exceptions and argument lists for subprocesses. Tests should cover observable outcomes and failure handling, not mirror wording. Never evaluate user-provided strings as code.

## Git and privacy

Prefer small conventional commits (`feat:`, `fix:`, `docs:`, `test:`, `chore:`). Use `codex/` for new work branches unless directed otherwise. Inspect status and staged changes; preserve unrelated work and history. Push when authorized, never force-push as a routine repair.

Do not commit credentials, personal machine paths, real learner records, local CLI state, build outputs, or complete chat logs. Keep git identity configuration local; do not add an email address to project files. Public project URLs and cited authors are intentional attribution. Never print suspected secret values in scan output.

There is no universal Vibe Coding file standard. These are this project's concrete AI-assisted development conventions, with reviewable diffs, tests and reproducible commands as the acceptance criteria.

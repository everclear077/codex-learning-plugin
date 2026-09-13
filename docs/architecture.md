# Architecture

## Layers

1. `.agents/plugins/marketplace.json` exposes `core-learning` at a repository-relative path.
2. `plugins/core-learning/.codex-plugin/plugin.json` declares display metadata and the bundled skills path.
3. `skills/learn-core/SKILL.md` establishes shared tutoring invariants and routes to references on demand.
4. References define five modes, course planning, progress records, Anki conversion and research provenance.
5. `export_anki.py` validates verified cards and converts them to TSV. The model and Anki remain external hosts.

There is no autonomous server, scheduler, model wrapper or secret store. AGENTS.md and CLAUDE.md govern development, not the learner's tutoring flow. Plugin packaging excludes repository maintenance files except its own license and README.

## Export data flow

JSON cards → validate schema/content/duplicates → escape HTML → TSV → user imports into Anki. IDs appear in tags for traceability; Anki duplicate matching uses the front field. Changing a front is not an ID-preserving update. Source text is displayed on the back, not fetched.

The exporter validates the entire input before opening the destination. Existing files are protected unless `--overwrite` is explicit. Tests cover Unicode, multiline fields, active HTML escaping, invalid input and protection against input/output collisions. Overwrite is a normal local file write, not a database transaction.

## Evidence model

Prompt-assisted success, independent success, transfer and delayed recall are distinct observations. Mode state includes a pending question and hint history. The model must not infer elapsed study time or recall difficulty from its own guess. Actual FSRS scheduling requires Anki or a separate genuine implementation, neither embedded here.

## Design choices

- Keep `core-learning` and `$learn-core` stable while the public repository is named `codex-learning-plugin`.
- Use a nested plugin directory so the repo can include CI and contributor documentation without shipping it to learners.
- Keep runtime dependencies at zero; PyYAML is development-only.
- Prefer explicit tests and documented manual scenarios over claims that static validation proves model behavior.

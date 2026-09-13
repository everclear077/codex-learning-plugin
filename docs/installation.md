# Installation, updates and troubleshooting

The repository is a marketplace containing one plugin. `core-learning` is the plugin ID, `codex-learning` the marketplace, and `learn-core` the skill. The UI title is 学习. Command syntax was checked against Codex CLI 0.153.4; check `codex plugin --help` on your installation.

## GitHub source

```sh
codex plugin marketplace add everclear077/codex-learning-plugin --ref main
codex plugin add core-learning@codex-learning
```

To follow a maintainer-published release tag instead, substitute that existing tag for `main`. Do not assume a tag exists just because the manifest contains a version. New tasks/sessions pick up the installed skills.

## Local development

Clone the repository, enter its root, then run:

```sh
codex plugin marketplace add .
codex plugin add core-learning@codex-learning
```

Local marketplace paths refer to the repository root, not its `.agents/plugins` directory. The entry's `./plugins/core-learning` path must stay inside that root. A plugin archive is useful for manual distribution, but this documentation does not invent a direct ZIP-install CLI command.

## Update and remove

For an installed Git marketplace:

```sh
codex plugin marketplace upgrade codex-learning
codex plugin add core-learning@codex-learning
```

For a local clone, update its files with your normal Git workflow and run the plugin-add command again after the manifest version changes. Use a new task. Public versions use semantic versioning; local cachebuster suffixes must remain uncommitted.

```sh
codex plugin remove core-learning@codex-learning
```

Removing the plugin does not delete your learning files. To change between local and remote marketplace sources, inspect `codex plugin marketplace list`, remove only this marketplace using the supported `marketplace remove` command, and add the intended source. Check `--help` before changing configured sources.

## Skill-only fallback

On a host supporting agent skills but not plugins, copy the **entire** `plugins/core-learning/skills/learn-core` folder to your chosen `.agents/skills/learn-core` directory (user or project scope supported by your host). Preserve `references`, `scripts` and `agents`. Do not overwrite an existing skill without checking it. This installs a skill, not a marketplace plugin; avoid installing duplicate copies simultaneously. Host skill discovery is documented in [Build skills](https://learn.chatgpt.com/docs/build-skills).

## Common problems

- `plugin` is unknown: install a Codex version that supports plugin commands; do not try unrelated marketplace syntax from another agent.
- Marketplace already exists: inspect its source before changing it. Do not register local and remote sources with the same name at once.
- Skill missing after installation: start a new task/session and check the plugin is enabled. Existing tasks may retain old instructions.
- Enterprise policy blocks a source: follow your administrator's rules; this plugin does not bypass them.
- Python is missing: tutoring still works; only the optional TSV exporter needs Python 3.10+.
- Export exists: select a new filename or deliberately use `--overwrite` after reviewing it.
- No Anki schedule: import the TSV and review in Anki; the plugin itself has not scheduled anything.

Official background: [Plugins](https://learn.chatgpt.com/docs/plugins). This repository's local integration checks exercise marketplace resolution and installation, not all product surfaces or account policies.

# Codex Learning Plugin

**Learn the essentials. Practice until you can.**

[中文](README.md) · [MIT license](LICENSE) · [Contributing](CONTRIBUTING.md)

A community Codex plugin that turns a topic into a measurable outcome, a small set of core concepts, guided practice, teach-back, spaced recall, and a real deliverable. Chinese is the default; the tutor follows the learner's language. This is not an official OpenAI project.

## Install

Requires Git and a Codex CLI with `codex plugin` support. Command syntax and local installation were verified with CLI 0.153.4.

```sh
codex plugin marketplace add everclear077/codex-learning-plugin --ref main
codex plugin add core-learning@codex-learning
```

Start a **new Codex task/session**, then invoke `$learn-core` or select the plugin displayed as **学习**. GitHub distribution does not imply listing in OpenAI's public catalog. See [installation and updates](docs/installation.md).

```text
Use $learn-core to teach me SQL in English. I have two hours.
My outcome: write and explain a report query using joins and aggregation.
Ask one question at a time. Give hints when I am wrong, then wait for my retry.
```

## Five separate modes

| Mode | Purpose |
|---|---|
| Socratic practice | One concept and one question; wait, hint, retry |
| Teach-back | Let the learner explain; identify gaps without rewriting the explanation |
| Fluency drills | Practice already-correct basics, then interleave related problem types |
| Project critique | Check a real artifact against agreed criteria; let the learner fix it |
| Spaced-recall quiz | Test older knowledge before giving hints or answers |

The tutor chooses 5–9 high-value concepts where appropriate, preserves required prerequisites, and names what to skip. A 20-hour sprint is a planning budget, not a mastery guarantee. Worked examples can help novices; an explicit request for a direct answer overrides the default tutoring posture. Seeing a solution never counts as independent success.

## Persistence and Anki

Longer courses can save progress in the learner's workspace under `learning/<topic-id>/`. The optional Python 3.10+ standard-library exporter creates Anki TSV files:

```sh
python plugins/core-learning/skills/learn-core/scripts/export_anki.py examples/cards.json cards.tsv
```

Import the file into Anki and review the field mapping. Anki performs actual FSRS scheduling. This plugin does not run a scheduler, import cards automatically, or send reminders. It has no custom telemetry or additional API-key requirement; Codex/model-provider and tool data policies still apply. [Privacy](PRIVACY.md)

## Development

```sh
python -m pip install -r requirements-dev.txt
python scripts/validate_repo.py
python -m unittest discover -s tests -v
python scripts/scan_public.py
python scripts/package_plugin.py
```

Read [AGENTS.md](AGENTS.md), [CLAUDE.md](CLAUDE.md), [architecture](docs/architecture.md), and [behavior evaluation scenarios](docs/behavior-evals.md). CI checks packaging and code; it does not measure learning outcomes. The detailed method report is currently in Chinese, with links to original sources.

## Attribution

Inspired by retrieval practice, teach-back, spacing, mastery learning, worked examples, and outcome-based planning, plus selected design ideas from three open-source learning skills. See [sources and scope](THIRD_PARTY_NOTICES.md). Original repository code is MIT-licensed; linked works retain their own licenses.

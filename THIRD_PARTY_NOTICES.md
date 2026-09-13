# Sources and attribution

The original code and documentation in this repository use the [MIT license](LICENSE). Linked research, books and external repositories retain their own licenses. Their inclusion as references does not relicense their contents or imply endorsement.

Selected design inspirations:

- [20-Hour AI Tutor Protocol](https://ceotudent.com/en/how-to-learn-anything-20-hours-ai-tutor-protocol): outcome-based sprint and tutor-mode framing.
- [learn-anything-24h](https://github.com/adityak74/learn-anything-24h): core scope, prerequisites, exercises and deliverables.
- [Superlearn](https://github.com/raiyanyahya/Superlearn): grounded research and structured learning maps.
- [mastery-loop](https://github.com/all666666all/mastery-loop): persistent learner evidence and recall workflows.
- [Anki manual](https://docs.ankiweb.net/importing/text-files.html): TSV import behavior; Anki and FSRS implementations are not bundled.

These are methodological references. This distribution does not vendor those repositories, reproduce complete third-party prompts or bundle paper PDFs. The detailed [method report](plugins/core-learning/skills/learn-core/references/方法梳理与溯源.md) identifies original studies and distinguishes results from local design choices. The exporter and repository tools are independently written for this project.

Development-only dependency: PyYAML (MIT), installed separately through `requirements-dev.txt`. GitHub Actions are fetched by CI under their respective licenses; their code is not included in the plugin archive.

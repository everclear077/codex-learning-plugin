# Contributing

Bug reports, teaching improvements, source corrections and translations are welcome. Use synthetic examples and redact private material. Discuss broad changes in an issue before implementing them; small fixes can go straight to a PR.

1. Fork/clone the repository and read [AGENTS.md](AGENTS.md).
2. Install `requirements-dev.txt` in your preferred Python environment.
3. Keep the change focused; update tests, examples and documentation when affected.
4. Run the four development commands in [README](README.md#开发与验证).
5. Describe the previous problem, resulting behavior, actual validation and any limitations in the PR.

AI assistance is welcome. Contributors are responsible for reviewing generated changes, checking citations and licenses, and ensuring no private data enters the diff. Do not submit generated test claims without execution evidence.

The skill defaults to Chinese and follows user language. Source corrections should link to primary research or the original project and distinguish published results from engineering choices. Do not add broad speed guarantees or silently change the five-mode contract.

See [release procedure](docs/releasing.md). Maintainers decide public version numbers for user-visible changes; personal development cachebuster suffixes must not enter published manifests.

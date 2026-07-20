# Changelog

All notable changes to this project are documented here. The format follows Keep a Changelog, and the project intends to use Semantic Versioning for published releases.

## [Unreleased]

## [1.0.0] - 2026-07-20

### Added

- Reusable integer-optimisation module aligned with the research formulation.
- Open-source PuLP/CBC solver support with optional Gurobi support.
- Synthetic example dataset and documented input schema.
- Paper-style risk-aversion experiment runner.
- CSV summaries, run metadata, SHA-256 input fingerprints and risk-return figures.
- Automated tests for constraints, validation, exclusions and reproducibility outputs.
- GitHub Actions verification on Python 3.9, 3.11 and 3.12.
- Automated source-distribution and wheel build validation with `build` and `twine`.
- Data-provenance guidance, Zenodo metadata and a release checklist.
- Installable project metadata and the `dream11-reproduce` command-line entry point.
- Research reuse guide covering extension studies, fair comparisons and data reporting.
- Contributor guidance focused on reproducible research changes.
- Structured issue template for reproduction attempts and comparison studies.

### Changed

- Removed Gurobi from mandatory dependencies.
- Added bounded dependency ranges for more stable CI.
- Relaxed numerical comparison tolerance to avoid false failures from harmless solver-level floating-point differences.
- Aligned the first stable GitHub release tag with package version `1.0.0`.
- Improved README discovery keywords, research-use cases and copy-ready citation guidance.

### Known limitation

- Exact reproduction of the paper's numerical results requires the original `Players_Score.csv`, which has not been recovered or publicly verified.

[Unreleased]: https://github.com/sauravsingla/Dream-11/compare/v1.0.0...HEAD
[1.0.0]: https://github.com/sauravsingla/Dream-11/releases/tag/v1.0.0

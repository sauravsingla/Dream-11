# Changelog

All notable changes to this project are documented here. The format follows Keep a Changelog, and the project intends to use Semantic Versioning for published releases.

## [Unreleased]

### Added

- Reusable integer-optimisation module aligned with the research formulation.
- Open-source PuLP/CBC solver support with optional Gurobi support.
- Synthetic example dataset and documented input schema.
- Paper-style risk-aversion experiment runner.
- CSV summaries, run metadata, SHA-256 input fingerprints and risk-return figures.
- Automated tests for constraints, validation, exclusions and reproducibility outputs.
- GitHub Actions verification across supported Python versions.
- Data-provenance guidance, Zenodo metadata and a release checklist.
- Installable project metadata and the `dream11-reproduce` command-line entry point.

### Changed

- Removed Gurobi from mandatory dependencies.
- Added bounded dependency ranges for more stable CI.
- Relaxed numerical comparison tolerance to avoid false failures from harmless solver-level floating-point differences.

### Known limitation

- Exact reproduction of the paper's numerical results requires the original `Players_Score.csv`, which has not been recovered or publicly verified.

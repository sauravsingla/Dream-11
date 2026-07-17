# Integer Optimisation for Dream 11 Cricket Team Selection

[![Tests](https://github.com/sauravsingla/Dream-11/actions/workflows/tests.yml/badge.svg)](https://github.com/sauravsingla/Dream-11/actions/workflows/tests.yml)
[![Python 3.9+](https://img.shields.io/badge/python-3.9%2B-blue.svg)](https://www.python.org/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

**Official research-code repository** for the article:

> Saurav Singla and Swapna Samir Shukla, **“Integer Optimisation for Dream 11 Cricket Team Selection,”** *International Journal of Computer Sciences and Engineering*, vol. 8, no. 11, pp. 1–6, November 2020.

**Research areas:** fantasy-sports analytics · cricket analytics · integer programming · portfolio optimisation · risk-aware optimisation · operations research · sports team selection · Python · Gurobi · PuLP

[Read the full text on ResearchGate](https://www.researchgate.net/publication/346564787_Integer_Optimisation_for_Dream_11_Cricket_Team_Selection) · [Run the example](#try-the-included-example) · [Reproduce experiments](#run-the-paper-style-experiments) · [Cite this work](#citation)

The study formulates fantasy-cricket team selection as a binary integer optimisation problem. It uses each player's performance over the previous ten matches and applies a Markowitz-inspired risk penalty to distinguish between risk-taking and risk-averse team-selection strategies.

## Why this repository may be useful

Researchers and practitioners can use this implementation as:

- a reproducible baseline for constrained fantasy-team selection;
- an example of transferring Markowitz-style risk modelling from finance to sports analytics;
- a starting point for comparisons with heuristics, evolutionary algorithms, machine learning or reinforcement learning;
- a teaching example for binary integer programming with real-world roster constraints.

When publishing results derived from this implementation, please cite the paper using the BibTeX entry below.

## Method implemented in the paper

For every available player, the model calculates:

- expected performance: mean fantasy score over the previous ten matches;
- performance risk: standard deviation of those ten scores;
- selection cost: the player's fantasy-credit price;
- player category and real-world team.

The objective maximises expected fantasy points after applying the captain and vice-captain multipliers, while penalising inconsistent players according to a user-selected risk-aversion coefficient.

The optimisation enforces the principal constraints described in the paper:

- exactly 11 selected players;
- exactly one captain and one vice-captain;
- captain score multiplier of 2.0 and vice-captain multiplier of 1.5;
- total cost not exceeding 100 credits;
- minimum and maximum counts for batsmen, bowlers, all-rounders and wicketkeepers;
- no more than seven players from one real-world team;
- a player can occupy at most one fantasy role.

## Repository contents

- `Dream_11.ipynb` — original research notebook and scenario analysis.
- `src/dream11_optimizer.py` — reusable implementation of the paper's optimisation model.
- `examples/run_optimisation.py` — command-line example for running the model on a CSV.
- `experiments/reproduce_paper_results.py` — repeatable risk-aversion experiment workflow.
- `data/example_players.csv` — clearly labelled synthetic data for trying the code.
- `data/README.md` — expected input schema.
- `docs/data_provenance.md` — rules for recovering or reconstructing the research data.
- `docs/research_reuse.md` — suggested extension studies and a fair comparison protocol.
- `docs/reproducibility_checklist.md` — environment, data, solver and reporting checks.
- `tests/` — PuLP-first tests for the optimisation and experiment workflows, with optional Gurobi coverage.
- `.github/workflows/tests.yml` — automated tests and reference-experiment verification.
- `pyproject.toml` — installable package and CLI configuration.
- `CITATION.bib` and `CITATION.cff` — copy-ready and machine-readable citation metadata.
- `CHANGELOG.md` — project change history.
- `.zenodo.json` — metadata prepared for a future archived software release.
- `RELEASE_CHECKLIST.md` — checks required before publishing `v1.0.0`.

The original notebook is retained as the historical research artefact. The reusable module removes the notebook's machine-specific file path and makes the model easier to run with another dataset.

## Expected input data

Provide one row per player with these columns:

```text
Player Name
Player Type
Team
Price
Retrospective Scores_1
...
Retrospective Scores_10
```

Supported player-type values are `BAT`, `BOWL`, `AR` and `WK`. The reusable implementation also accepts common aliases such as `Bowler`, `Batsman`, `All-Rounder` and `Wicketkeeper`.

## Installation

Python 3.9 or later is supported.

For an editable development installation with test dependencies:

```bash
python -m venv .venv
source .venv/bin/activate       # Windows: .venv\Scripts\activate
pip install -e ".[test]"
```

For a regular open-source PuLP/CBC installation:

```bash
pip install .
```

The legacy requirements-file workflow remains available:

```bash
pip install -r requirements.txt
```

To install the optional Gurobi backend:

```bash
pip install -e ".[gurobi]"
```

Gurobi requires an appropriate licence. It is not required to run the examples, tests or reproduction workflow with PuLP.

The implementation supports two solver backends:

- **Gurobi**, matching the solver used by the original research notebook. It requires a valid licence.
- **PuLP with CBC**, the default open-source option that works without a commercial solver licence.

With `solver="auto"`, the code tries Gurobi first and falls back to PuLP when Gurobi is unavailable.

## Try the included example

```bash
python examples/run_optimisation.py data/example_players.csv \
  --solver pulp \
  --risk-aversion 2
```

The example dataset is synthetic and is provided only to demonstrate the workflow. It is not the dataset used to generate the paper's reported results.

## Run the paper-style experiments

After installation, use the packaged CLI:

```bash
dream11-reproduce \
  --input data/example_players.csv \
  --solver pulp \
  --risk-values 0 0.5 1 2 5 10
```

The Python script remains available directly:

```bash
python experiments/reproduce_paper_results.py \
  --input data/example_players.csv \
  --solver pulp \
  --risk-values 0 0.5 1 2 5 10
```

Generated outputs include:

- `experiment_summary.csv`;
- `run_metadata.json` with an input-file SHA-256 fingerprint and package versions;
- one selected-team CSV per risk-aversion value;
- `expected_score_vs_risk_aversion.png`;
- `team_risk_vs_risk_aversion.png`.

To repeat the paper's player-unavailability scenario on a compatible dataset, add:

```bash
--exclude-player "V Kohli"
```

By default, outputs are written under `outputs/paper_experiments/`. Exact numerical reproduction requires the verified original research dataset.

## Run with another CSV

```bash
python examples/run_optimisation.py data/players.csv \
  --solver auto \
  --risk-aversion 2 \
  --output outputs/selected_team.csv
```

The command prints the selected eleven with captain and vice-captain assignments. When `--output` is supplied, it also writes the complete result to a CSV file.

## Use from Python

```python
import pandas as pd

from src import OptimisationConfig, optimise_team

players = pd.read_csv("data/example_players.csv")
config = OptimisationConfig(risk_aversion=2.0, solver="pulp")
team = optimise_team(players, config)

print(team[["Player Name", "Player Type", "Fantasy Role", "Expected Score"]])
```

## Reproducing the paper

To reproduce the exact numerical tables and selected teams from the article, use the same player scores and prices used in the original experiment. The original local source file was not committed and no verified public copy has been identified. See `docs/data_provenance.md` before adding recovered or reconstructed data.

## Archival release

The repository contains Zenodo metadata and a release checklist, but a software DOI has not yet been issued. A DOI should be added only after a reviewed GitHub release is published and successfully archived by Zenodo.

## Citation

Please cite the article when using this implementation, model formulation, experiment design or derivative datasets in academic work. The [full text is available on ResearchGate](https://www.researchgate.net/publication/346564787_Integer_Optimisation_for_Dream_11_Cricket_Team_Selection).

```bibtex
@article{singla2020integer,
  title   = {Integer Optimisation for Dream 11 Cricket Team Selection},
  author  = {Singla, Saurav and Shukla, Swapna Samir},
  journal = {International Journal of Computer Sciences and Engineering},
  volume  = {8},
  number  = {11},
  pages   = {1--6},
  year    = {2020},
  month   = {November},
  doi     = {10.26438/ijcse/v8i11.16}
}
```

A standalone BibTeX record is available in `CITATION.bib`. Machine-readable citation metadata is provided in `CITATION.cff`, and GitHub's **Cite this repository** control can generate additional citation formats.

## Contributing

Research reproductions, alternative optimisation methods, dataset adapters and documentation improvements are welcome. Please read `CONTRIBUTING.md` before opening a pull request.

## Disclaimer

This repository is an academic demonstration of constrained optimisation. It does not guarantee contest winnings and is not affiliated with or endorsed by Dream11.

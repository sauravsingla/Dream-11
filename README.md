# Integer Optimisation for Dream 11 Cricket Team Selection

This repository contains the code accompanying the research article:

> Saurav Singla and Swapna Samir Shukla, **“Integer Optimisation for Dream 11 Cricket Team Selection,”** *International Journal of Computer Sciences and Engineering*, vol. 8, no. 11, pp. 1–6, November 2020. DOI: [10.26438/ijcse/v8i11.16](https://doi.org/10.26438/ijcse/v8i11.16).

The study formulates fantasy-cricket team selection as a binary integer optimisation problem. It uses each player's performance over the previous ten matches and applies a Markowitz-inspired risk penalty to distinguish between risk-taking and risk-averse team-selection strategies.

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
- `data/example_players.csv` — clearly labelled synthetic data for trying the code.
- `data/README.md` — expected data schema and provenance guidance.
- `tests/` — synthetic tests for the main team-selection constraints.
- `.github/workflows/tests.yml` — automated tests for supported Python versions.

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

Python 3.9 or later is recommended.

```bash
python -m venv .venv
source .venv/bin/activate       # Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

The implementation supports two solver backends:

- **Gurobi**, matching the solver used by the original research notebook. It requires a valid licence.
- **PuLP with CBC**, an open-source option that works without a commercial solver licence.

With `solver="auto"`, the code tries Gurobi first and falls back to PuLP when Gurobi is unavailable.

## Try the included example

```bash
python examples/run_optimisation.py data/example_players.csv \
  --solver pulp \
  --risk-aversion 2
```

The example dataset is synthetic and is provided only to demonstrate the workflow. It is not the dataset used to generate the paper's reported results.

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

from src.dream11_optimizer import OptimisationConfig, optimise_team

players = pd.read_csv("data/example_players.csv")
config = OptimisationConfig(risk_aversion=2.0, solver="pulp")
team = optimise_team(players, config)

print(team[["Player Name", "Player Type", "Fantasy Role", "Expected Score"]])
```

## Reproducing the paper

To reproduce the exact numerical tables and selected teams from the article, use the same player scores and prices used in the original experiment. Those values are visible in the executed notebook output, but the original local source file was not committed. No replacement dataset is presented here as the original data unless its provenance can be verified.

## Citation

Please cite the article when using this implementation in academic work. Machine-readable citation metadata is provided in `CITATION.cff`.

## Disclaimer

This repository is an academic demonstration of constrained optimisation. It does not guarantee contest winnings and is not affiliated with or endorsed by Dream11.

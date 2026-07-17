# Player data

The optimiser expects a CSV with one row per candidate player and these fields:

- `Player Name`
- `Player Type`
- `Team`
- `Price`
- `Retrospective Scores_1` through `Retrospective Scores_10`

`Player Type` should identify a batsman, bowler, all-rounder or wicketkeeper. The reusable implementation accepts the short forms `BAT`, `BOWL`, `AR` and `WK`, together with common long-form aliases.

## Original research data

The historical player-score file used for the 2020 paper was loaded by the notebook from a local Windows path and was not committed to this repository. It is therefore not included here as an original research dataset.

For an exact reproduction of the paper's reported teams, use the same player scores, categories and prices from the study. For demonstrations or extensions, create a new CSV using the schema above and state its source clearly.

Local CSV files under this directory are ignored by Git so that private or licensed sports data is not committed accidentally.

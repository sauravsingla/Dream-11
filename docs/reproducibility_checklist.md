# Reproducibility checklist

Use this checklist when reproducing the examples, comparing another method with this implementation, or reporting results derived from the repository.

## Environment

- [ ] Record the operating system and version.
- [ ] Use Python 3.9 or later.
- [ ] Record the exact Python version.
- [ ] Install the project with `pip install -e ".[test]"` or record an equivalent installation procedure.
- [ ] Save the installed package versions, for example with `python -m pip freeze > environment.txt`.

## Solver

- [ ] Record whether the run used Gurobi or PuLP/CBC.
- [ ] Record the solver version.
- [ ] Record any non-default solver settings, time limits or optimality gaps.
- [ ] Confirm that the solver returned an optimal solution before comparing results.

## Input data

- [ ] Use one row per player and follow the schema in `data/README.md`.
- [ ] Confirm that every player has a name, player type, team and credit price.
- [ ] Confirm that all ten retrospective-score columns are present.
- [ ] Record whether the data are original, public, reconstructed or synthetic.
- [ ] Preserve the input-file SHA-256 fingerprint written to `run_metadata.json`.
- [ ] Do not describe the synthetic example dataset as the dataset used in the published paper.

## Experiment configuration

- [ ] Record all risk-aversion values.
- [ ] Record any excluded player used for an unavailability scenario.
- [ ] Record the roster, budget and team constraints if they differ from the defaults.
- [ ] Record the exact command or Python configuration used for each run.
- [ ] Record a random seed for any comparison method that uses randomness. The integer-programming model itself is deterministic for a fixed input and solver configuration.

## Expected outputs

A complete experiment run should normally produce:

- [ ] `experiment_summary.csv`;
- [ ] `run_metadata.json`;
- [ ] one selected-team CSV for every risk-aversion value;
- [ ] `expected_score_vs_risk_aversion.png`;
- [ ] `team_risk_vs_risk_aversion.png`.

## Validation

- [ ] Confirm that every selected team contains exactly 11 players.
- [ ] Confirm that each team contains exactly one captain and one vice-captain.
- [ ] Confirm that the total credit cost is at most 100.
- [ ] Confirm that player-type bounds are satisfied.
- [ ] Confirm that no more than seven players come from one real-world team.
- [ ] Run `pytest` and report any failing tests.

## Reporting limitations

- [ ] State clearly when exact numerical reproduction is not possible because the verified original research dataset is unavailable.
- [ ] Distinguish reproduction of the method from reproduction of the paper's exact numerical tables.
- [ ] Cite the associated article and link to the exact repository release or commit used.

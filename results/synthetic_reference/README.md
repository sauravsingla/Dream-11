# Synthetic reference experiment

This directory contains the validated summary generated from `data/example_players.csv` with PuLP/CBC and the following command:

```bash
python experiments/reproduce_paper_results.py \
  --input data/example_players.csv \
  --solver pulp \
  --risk-values 0 0.5 1 2 5 10 \
  --output-dir outputs/paper_experiments
```

The committed `experiment_summary.csv` is a reproducibility reference for the software workflow. It is **not** a reproduction of the numerical results in the 2020 paper because the original `Players_Score.csv` has not yet been recovered.

## Observed behaviour

- The synthetic optimum uses the full 100-credit budget for risk values 0 through 5 and 99 credits at risk value 10.
- The captain remains `Example Allrounder C` and the vice-captain remains `Example Allrounder A` for all tested values.
- Increasing risk aversion changes the selected supporting players and reduces total team risk from about 58.58 to 53.78.
- Every generated team satisfies the required composition of 11 players, one captain, one vice-captain, role limits, the budget and the seven-player real-team limit.

Small floating-point differences in the final decimal places may occur across solver or library versions. Team composition, captaincy and constraint compliance are the primary reproducibility checks.

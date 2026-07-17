# Research reuse and extension guide

This document describes ways to build on the paper while keeping comparisons transparent and reproducible.

## Suitable uses of this implementation

The optimiser can serve as a baseline for studies involving:

- constrained fantasy-cricket team selection;
- risk-aware sports analytics;
- binary integer programming for roster construction;
- comparisons between exact optimisation and heuristic methods;
- sensitivity analysis for player price, recent form and risk aversion;
- transfer of portfolio-optimisation ideas to sports selection.

## Suggested extension studies

Potential research directions include:

1. **Alternative optimisation methods** — compare the exact integer-programming solution with genetic algorithms, simulated annealing, particle swarm optimisation or greedy heuristics.
2. **Predictive scoring models** — replace the ten-match mean with regression, gradient boosting, Bayesian forecasting or sequence models, while retaining the same roster constraints.
3. **Uncertainty-aware selection** — model score distributions, prediction intervals or scenario-based robust optimisation rather than a single expected score and standard deviation.
4. **Multi-objective optimisation** — study trade-offs among expected points, downside risk, player ownership, diversity and budget utilisation.
5. **Temporal evaluation** — use rolling, leakage-free train/test windows across multiple seasons and report performance match by match.
6. **Cross-sport adaptation** — adapt the formulation to football, basketball or other fantasy-sport roster rules.

These are suggestions for independent follow-up work, not claims made by the original article.

## Fair comparison protocol

A useful comparison should hold the following elements constant across methods:

- the same player pool and pre-match information;
- the same fantasy scoring rules;
- the same budget, role and team constraints;
- the same captain and vice-captain rules;
- the same temporal split, without using information from or after the target match;
- the same number of optimisation runs for stochastic methods.

At minimum, report:

- realised fantasy points of the selected team;
- predicted or expected fantasy points;
- team-level risk measure;
- constraint feasibility rate;
- runtime and computing environment;
- random seeds for stochastic algorithms;
- mean, standard deviation and confidence interval across target matches.

## Data reporting checklist

When sharing a new dataset or benchmark, document:

- competition and season;
- date range and number of matches;
- source and licence or terms of use;
- player-price source;
- fantasy scoring rules;
- missing-data treatment;
- exact feature availability time;
- train, validation and test split construction;
- checks used to prevent look-ahead leakage.

Do not describe reconstructed or synthetic data as the original research dataset. Clearly label all derived datasets and record the transformation steps used to create them.

## Referencing the baseline

When the model, formulation, constraints or experiment design from this repository is used in a publication, cite the associated article:

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

For reproducibility, also record the repository commit SHA or a future archived software release DOI.
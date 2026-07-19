# Fantasy Cricket Team Optimisation with Python

This guide explains how the Dream-11 repository solves fantasy cricket team selection as a constrained optimisation problem in Python.

## What problem does this project solve?

The software selects an optimal fantasy cricket squad from a pool of available players. It considers expected fantasy points, recent performance variability, player price, cricket role, real-world team, captain selection and vice-captain selection.

The model is useful for searches and research involving:

- Dream11 team prediction using Python;
- fantasy cricket team optimisation;
- fantasy cricket lineup generation;
- optimal player selection under a credit budget;
- captain and vice-captain optimisation;
- cricket squad selection using operations research;
- binary integer linear programming for sports analytics;
- ILP and MILP models for roster optimisation;
- risk-aware fantasy sports decision support.

## Optimisation approach

Each player is represented by binary decision variables indicating whether the player is selected and whether the player is assigned as captain or vice-captain. The objective maximises expected fantasy points while applying a configurable penalty for inconsistent historical performance.

The formulation belongs to the family of:

- integer linear programming (ILP);
- binary integer programming;
- mixed-integer linear programming (MILP);
- combinatorial optimisation;
- constrained roster and lineup optimisation;
- mathematical programming for sports analytics.

## Constraints represented

The implementation supports the central constraints described in the associated research paper:

- exactly eleven selected players;
- one captain and one vice-captain;
- a maximum fantasy-credit budget;
- minimum and maximum counts for batsmen, bowlers, all-rounders and wicketkeepers;
- a limit on players selected from one real-world team;
- mutually exclusive fantasy roles for each player.

## Risk-aware team selection

The project adapts a Markowitz-style idea from portfolio optimisation. A player's average score represents expected return, while the standard deviation of recent scores represents performance risk. Increasing the risk-aversion parameter favours more consistent players; decreasing it allows more volatile, higher-upside selections.

## Solvers

The reusable Python implementation supports:

- PuLP with the open-source CBC solver;
- Gurobi when a valid commercial or academic licence is available.

PuLP/CBC is sufficient for the included example, automated tests and reproducibility workflow.

## Typical research extensions

This repository can be used as a baseline for comparing integer programming with:

- greedy and heuristic team-selection algorithms;
- genetic algorithms and evolutionary optimisation;
- machine-learning player projections;
- reinforcement-learning selection strategies;
- robust and stochastic optimisation;
- multi-objective optimisation of score, risk and player diversity.

## Associated publication

Saurav Singla and Swapna Samir Shukla, "Integer Optimisation for Dream 11 Cricket Team Selection," International Journal of Computer Sciences and Engineering, 2020.

Paper DOI: `10.26438/ijcse/v8i11.16`

See the repository README for installation, runnable examples, reproducibility instructions and citation metadata.

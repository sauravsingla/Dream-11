# Frequently Asked Questions

## What is this Dream11 optimisation project?

It is an open-source Python implementation of a research model for selecting a fantasy cricket team with binary integer programming. The model balances expected fantasy points, player consistency, credit limits, cricket roles and captain or vice-captain multipliers.

## Can this code generate a fantasy cricket team?

Yes. Given a compatible CSV containing player names, roles, teams, prices and recent fantasy scores, the software selects eleven players and assigns a captain and vice-captain.

## Is this a Dream11 prediction algorithm?

It is better described as a constrained team-selection and optimisation model. It does not predict match outcomes or guarantee contest winnings. It uses historical fantasy scores as inputs and solves the resulting lineup-selection problem mathematically.

## Which optimisation method is used?

The project uses binary integer programming, also commonly described as integer linear programming (ILP), mixed-integer linear programming (MILP), mathematical optimisation or combinatorial optimisation.

## Which Python solvers are supported?

The code supports PuLP with CBC and optionally Gurobi. PuLP/CBC is the default open-source route and does not require a commercial solver licence.

## How is player risk measured?

The model uses the standard deviation of a player's recent fantasy scores as a measure of performance variability. A risk-aversion parameter controls how strongly inconsistent players are penalised.

## Does the model choose the captain and vice-captain?

Yes. Captain and vice-captain assignments are part of the optimisation model, including the corresponding score multipliers.

## What constraints are included?

The implementation covers squad size, total credits, player-role limits, real-team limits, captain and vice-captain selection, and mutually exclusive fantasy roles.

## Can I use my own player data?

Yes. The repository documents the required CSV columns and includes a synthetic example dataset. Exact reproduction of the published numerical results requires the original research inputs, which are not included as a verified public dataset.

## Is this project useful for research?

Yes. It can serve as a reproducible baseline for fantasy sports analytics, sports operations research, lineup optimisation, roster selection, risk-aware decision support and comparisons with heuristics, machine learning, evolutionary algorithms or reinforcement learning.

## How should I cite the project?

Use the citation shown in `README.md`, `CITATION.cff` or `CITATION.bib`. The associated paper DOI is `10.26438/ijcse/v8i11.16`.

## Is this repository affiliated with Dream11?

No. It is an independent academic and software demonstration and is not affiliated with or endorsed by Dream11.

"""Reusable implementation of the Dream11 integer-optimisation model.

The formulation follows Singla and Shukla (2020): expected player scores are
estimated from the previous ten matches and inconsistent performance is
penalised through a Markowitz-inspired risk-aversion term.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Mapping

import numpy as np
import pandas as pd

try:
    import gurobipy as gp
    from gurobipy import GRB
except ImportError:  # pragma: no cover
    gp = None
    GRB = None

try:
    import pulp
except ImportError:  # pragma: no cover
    pulp = None


PLAYER_TYPE_ALIASES = {
    "BAT": "BAT",
    "BATSMAN": "BAT",
    "BATTER": "BAT",
    "BOWL": "BOWL",
    "BOWLER": "BOWL",
    "AR": "AR",
    "ALLROUNDER": "AR",
    "ALL-ROUNDER": "AR",
    "ALL ROUNDER": "AR",
    "WK": "WK",
    "WICKETKEEPER": "WK",
    "WICKET-KEEPER": "WK",
    "WICKET KEEPER": "WK",
}

ROLES = ("PLAYER", "VICE_CAPTAIN", "CAPTAIN")
MULTIPLIERS = {"PLAYER": 1.0, "VICE_CAPTAIN": 1.5, "CAPTAIN": 2.0}
ROLE_COUNTS = {"PLAYER": 9, "VICE_CAPTAIN": 1, "CAPTAIN": 1}


@dataclass(frozen=True)
class OptimisationConfig:
    """Parameters controlling the paper-aligned team-selection model."""

    risk_aversion: float = 0.0
    budget: float = 100.0
    max_players_per_team: int = 7
    solver: str = "auto"
    role_limits: Mapping[str, tuple[int, int]] = field(
        default_factory=lambda: {
            "BAT": (3, 6),
            "BOWL": (3, 6),
            "AR": (1, 4),
            "WK": (1, 4),
        }
    )
    score_columns: tuple[str, ...] = tuple(
        f"Retrospective Scores_{index}" for index in range(1, 11)
    )

    def __post_init__(self) -> None:
        if self.risk_aversion < 0:
            raise ValueError("risk_aversion must be non-negative")
        if self.budget <= 0:
            raise ValueError("budget must be positive")
        if self.max_players_per_team < 1:
            raise ValueError("max_players_per_team must be at least 1")
        if self.solver.lower() not in {"auto", "gurobi", "pulp"}:
            raise ValueError("solver must be one of: auto, gurobi, pulp")
        for player_type, bounds in self.role_limits.items():
            if len(bounds) != 2 or bounds[0] < 0 or bounds[1] < bounds[0]:
                raise ValueError(f"Invalid limits for {player_type}: {bounds}")


def _normalise_player_type(value: object) -> str:
    key = str(value).strip().upper()
    try:
        return PLAYER_TYPE_ALIASES[key]
    except KeyError as exc:
        supported = ", ".join(sorted({"BAT", "BOWL", "AR", "WK"}))
        raise ValueError(
            f"Unsupported player type {value!r}; expected one of {supported}"
        ) from exc


def prepare_player_data(
    players: pd.DataFrame, config: OptimisationConfig | None = None
) -> pd.DataFrame:
    """Validate player data and calculate the paper's mean and risk vectors."""

    config = config or OptimisationConfig()
    required = {"Player Name", "Player Type", "Team", "Price", *config.score_columns}
    missing = sorted(required.difference(players.columns))
    if missing:
        raise ValueError(f"Missing required columns: {', '.join(missing)}")

    prepared = players.copy()
    prepared["Player Type"] = prepared["Player Type"].map(_normalise_player_type)
    prepared["Price"] = pd.to_numeric(prepared["Price"], errors="raise")
    prepared.loc[:, config.score_columns] = prepared.loc[
        :, config.score_columns
    ].apply(pd.to_numeric, errors="raise")

    if prepared["Player Name"].duplicated().any():
        duplicates = prepared.loc[
            prepared["Player Name"].duplicated(), "Player Name"
        ].tolist()
        raise ValueError(f"Duplicate player names are not supported: {duplicates}")
    if (prepared["Price"] <= 0).any():
        raise ValueError("Every player price must be positive")
    if prepared.loc[:, config.score_columns].isna().any().any():
        raise ValueError("Historical score columns cannot contain missing values")

    score_matrix = prepared.loc[:, config.score_columns].to_numpy(dtype=float)
    prepared["Expected Score"] = np.mean(score_matrix, axis=1)
    prepared["Score Risk"] = np.std(score_matrix, axis=1, ddof=0)
    return prepared


def _build_result(
    prepared: pd.DataFrame,
    chosen_roles: Mapping[tuple[str, object], bool],
    config: OptimisationConfig,
) -> pd.DataFrame:
    chosen: list[dict[str, object]] = []
    for role in ROLES:
        for index in prepared.index:
            if chosen_roles.get((role, index), False):
                row = prepared.loc[index].to_dict()
                row["Fantasy Role"] = role
                row["Score Multiplier"] = MULTIPLIERS[role]
                row["Risk-adjusted Contribution"] = (
                    MULTIPLIERS[role] * row["Expected Score"]
                    - config.risk_aversion * row["Score Risk"]
                )
                chosen.append(row)

    result = pd.DataFrame(chosen)
    role_order = pd.CategoricalDtype(
        ["CAPTAIN", "VICE_CAPTAIN", "PLAYER"], ordered=True
    )
    result["Fantasy Role"] = result["Fantasy Role"].astype(role_order)
    return result.sort_values(
        ["Fantasy Role", "Risk-adjusted Contribution"], ascending=[True, False]
    ).reset_index(drop=True)


def _optimise_with_gurobi(
    prepared: pd.DataFrame, config: OptimisationConfig
) -> pd.DataFrame:
    if gp is None or GRB is None:
        raise RuntimeError("Gurobi is not installed")

    indices = list(prepared.index)
    model = gp.Model("dream11_team_selection")
    model.Params.OutputFlag = 0
    selected = model.addVars(ROLES, indices, vtype=GRB.BINARY, name="selected")

    model.setObjective(
        gp.quicksum(
            (
                MULTIPLIERS[role] * prepared.at[index, "Expected Score"]
                - config.risk_aversion * prepared.at[index, "Score Risk"]
            )
            * selected[role, index]
            for role in ROLES
            for index in indices
        ),
        GRB.MAXIMIZE,
    )

    for index in indices:
        model.addConstr(gp.quicksum(selected[role, index] for role in ROLES) <= 1)
    for role in ROLES:
        model.addConstr(
            gp.quicksum(selected[role, index] for index in indices)
            == ROLE_COUNTS[role]
        )
    model.addConstr(
        gp.quicksum(
            prepared.at[index, "Price"] * selected[role, index]
            for role in ROLES
            for index in indices
        )
        <= config.budget
    )
    for player_type, (minimum, maximum) in config.role_limits.items():
        matching = prepared.index[prepared["Player Type"] == player_type].tolist()
        count = gp.quicksum(
            selected[role, index] for role in ROLES for index in matching
        )
        model.addConstr(count >= minimum)
        model.addConstr(count <= maximum)
    for _, group in prepared.groupby("Team"):
        model.addConstr(
            gp.quicksum(
                selected[role, index]
                for role in ROLES
                for index in group.index.tolist()
            )
            <= config.max_players_per_team
        )

    model.optimize()
    if model.Status == GRB.INFEASIBLE:
        raise ValueError("No feasible team satisfies the supplied constraints")
    if model.Status != GRB.OPTIMAL:
        raise RuntimeError(f"Gurobi stopped with status {model.Status}")

    chosen = {
        (role, index): selected[role, index].X > 0.5
        for role in ROLES
        for index in indices
    }
    return _build_result(prepared, chosen, config)


def _optimise_with_pulp(
    prepared: pd.DataFrame, config: OptimisationConfig
) -> pd.DataFrame:
    if pulp is None:
        raise RuntimeError("PuLP is not installed")

    indices = list(prepared.index)
    model = pulp.LpProblem("dream11_team_selection", pulp.LpMaximize)
    selected = {
        (role, index): pulp.LpVariable(
            f"selected_{role.lower()}_{index}", cat="Binary"
        )
        for role in ROLES
        for index in indices
    }

    model += pulp.lpSum(
        (
            MULTIPLIERS[role] * prepared.at[index, "Expected Score"]
            - config.risk_aversion * prepared.at[index, "Score Risk"]
        )
        * selected[role, index]
        for role in ROLES
        for index in indices
    )

    for index in indices:
        model += pulp.lpSum(selected[role, index] for role in ROLES) <= 1
    for role in ROLES:
        model += (
            pulp.lpSum(selected[role, index] for index in indices)
            == ROLE_COUNTS[role]
        )
    model += (
        pulp.lpSum(
            prepared.at[index, "Price"] * selected[role, index]
            for role in ROLES
            for index in indices
        )
        <= config.budget
    )
    for player_type, (minimum, maximum) in config.role_limits.items():
        matching = prepared.index[prepared["Player Type"] == player_type].tolist()
        count = pulp.lpSum(
            selected[role, index] for role in ROLES for index in matching
        )
        model += count >= minimum
        model += count <= maximum
    for _, group in prepared.groupby("Team"):
        model += (
            pulp.lpSum(
                selected[role, index]
                for role in ROLES
                for index in group.index.tolist()
            )
            <= config.max_players_per_team
        )

    status = model.solve(pulp.PULP_CBC_CMD(msg=False))
    if status == pulp.LpStatusInfeasible:
        raise ValueError("No feasible team satisfies the supplied constraints")
    if status != pulp.LpStatusOptimal:
        raise RuntimeError(f"PuLP stopped with status {pulp.LpStatus[status]}")

    chosen = {
        key: bool(variable.value() and variable.value() > 0.5)
        for key, variable in selected.items()
    }
    return _build_result(prepared, chosen, config)


def optimise_team(
    players: pd.DataFrame,
    config: OptimisationConfig | None = None,
) -> pd.DataFrame:
    """Select the optimal eleven and assign captain/vice-captain roles.

    ``solver='auto'`` prefers Gurobi when it is installed and falls back to
    PuLP's open-source CBC solver. Set ``solver='gurobi'`` or ``solver='pulp'``
    to select a backend explicitly.
    """

    config = config or OptimisationConfig()
    prepared = prepare_player_data(players, config)
    if len(prepared) < 11:
        raise ValueError("At least 11 candidate players are required")

    solver = config.solver.lower()
    if solver == "gurobi":
        return _optimise_with_gurobi(prepared, config)
    if solver == "pulp":
        return _optimise_with_pulp(prepared, config)

    if gp is not None and GRB is not None:
        try:
            return _optimise_with_gurobi(prepared, config)
        except Exception as exc:
            if pulp is None:
                raise RuntimeError(
                    "Gurobi could not solve the model and PuLP is unavailable"
                ) from exc
    if pulp is not None:
        return _optimise_with_pulp(prepared, config)
    raise RuntimeError("Install either gurobipy or pulp to solve the model")

import pandas as pd
import pytest

from src.dream11_optimizer import (
    OptimisationConfig,
    optimise_team,
    prepare_player_data,
)


def make_players() -> pd.DataFrame:
    rows = []
    player_types = ["BAT"] * 5 + ["BOWL"] * 5 + ["AR"] * 3 + ["WK"] * 3
    for index, player_type in enumerate(player_types):
        row = {
            "Player Name": f"Player {index + 1}",
            "Player Type": player_type,
            "Team": "INDIA" if index % 2 == 0 else "ENGLAND",
            "Price": 8.0,
        }
        for match in range(1, 11):
            row[f"Retrospective Scores_{match}"] = 40 + index * 3 + match
        rows.append(row)
    return pd.DataFrame(rows)


def assert_paper_constraints(team: pd.DataFrame) -> None:
    assert len(team) == 11
    assert team["Price"].sum() <= 100
    assert (team["Fantasy Role"] == "CAPTAIN").sum() == 1
    assert (team["Fantasy Role"] == "VICE_CAPTAIN").sum() == 1
    assert team.groupby("Team").size().max() <= 7

    type_counts = team.groupby("Player Type").size().to_dict()
    assert 3 <= type_counts["BAT"] <= 6
    assert 3 <= type_counts["BOWL"] <= 6
    assert 1 <= type_counts["AR"] <= 4
    assert 1 <= type_counts["WK"] <= 4


def test_prepare_player_data_calculates_mean_and_population_risk() -> None:
    prepared = prepare_player_data(make_players())

    assert prepared.loc[0, "Expected Score"] == pytest.approx(45.5)
    assert prepared.loc[0, "Score Risk"] == pytest.approx(2.872281323)


def test_prepare_player_data_normalises_common_role_names() -> None:
    players = make_players()
    players.loc[0, "Player Type"] = "Batsman"
    players.loc[5, "Player Type"] = "Bowler"
    players.loc[10, "Player Type"] = "All-Rounder"
    players.loc[13, "Player Type"] = "Wicketkeeper"

    prepared = prepare_player_data(players)

    assert set(prepared["Player Type"]) == {"BAT", "BOWL", "AR", "WK"}


def test_prepare_player_data_rejects_missing_score_columns() -> None:
    players = make_players().drop(columns=["Retrospective Scores_10"])

    with pytest.raises(ValueError, match="Missing required columns"):
        prepare_player_data(players)


def test_pulp_optimised_team_obeys_paper_constraints() -> None:
    pytest.importorskip("pulp")
    team = optimise_team(
        make_players(),
        OptimisationConfig(risk_aversion=1.0, solver="pulp"),
    )
    assert_paper_constraints(team)


def test_gurobi_optimised_team_obeys_paper_constraints_when_available() -> None:
    pytest.importorskip("gurobipy")
    team = optimise_team(
        make_players(),
        OptimisationConfig(risk_aversion=1.0, solver="gurobi"),
    )
    assert_paper_constraints(team)

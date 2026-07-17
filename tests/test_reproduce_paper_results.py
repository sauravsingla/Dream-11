import json
from pathlib import Path

import pandas as pd
import pytest

from experiments.reproduce_paper_results import file_sha256, run_experiments


EXAMPLE_DATA = Path("data/example_players.csv")


def test_file_sha256_is_stable() -> None:
    first = file_sha256(EXAMPLE_DATA)
    second = file_sha256(EXAMPLE_DATA)

    assert first == second
    assert len(first) == 64


def test_run_experiments_generates_reproducibility_outputs(tmp_path: Path) -> None:
    output_dir = tmp_path / "results"

    summary = run_experiments(
        input_path=EXAMPLE_DATA,
        risk_values=[0.0, 2.0],
        budget=100.0,
        solver="pulp",
        excluded_players=[],
        output_dir=output_dir,
    )

    assert list(summary["risk_aversion"]) == [0.0, 2.0]
    assert (output_dir / "experiment_summary.csv").exists()
    assert (output_dir / "run_metadata.json").exists()
    assert (output_dir / "selected_team_risk_0.csv").exists()
    assert (output_dir / "selected_team_risk_2.csv").exists()
    assert (output_dir / "expected_score_vs_risk_aversion.png").exists()
    assert (output_dir / "team_risk_vs_risk_aversion.png").exists()

    metadata = json.loads((output_dir / "run_metadata.json").read_text())
    assert metadata["input_sha256"] == file_sha256(EXAMPLE_DATA)
    assert metadata["solver"] == "pulp"
    assert metadata["risk_values"] == [0.0, 2.0]
    assert "matplotlib_version" in metadata


def test_run_experiments_rejects_duplicate_risk_values(tmp_path: Path) -> None:
    with pytest.raises(ValueError, match="must be unique"):
        run_experiments(
            input_path=EXAMPLE_DATA,
            risk_values=[1.0, 1.0],
            budget=100.0,
            solver="pulp",
            excluded_players=[],
            output_dir=tmp_path,
        )


def test_run_experiments_rejects_negative_risk_values(tmp_path: Path) -> None:
    with pytest.raises(ValueError, match="non-negative"):
        run_experiments(
            input_path=EXAMPLE_DATA,
            risk_values=[-1.0],
            budget=100.0,
            solver="pulp",
            excluded_players=[],
            output_dir=tmp_path,
        )


def test_run_experiments_rejects_unknown_excluded_player(tmp_path: Path) -> None:
    with pytest.raises(ValueError, match="Excluded player not present"):
        run_experiments(
            input_path=EXAMPLE_DATA,
            risk_values=[0.0],
            budget=100.0,
            solver="pulp",
            excluded_players=["Unknown Player"],
            output_dir=tmp_path,
        )


def test_run_experiments_records_player_exclusion(tmp_path: Path) -> None:
    excluded = "Example Batter F"
    output_dir = tmp_path / "excluded"

    run_experiments(
        input_path=EXAMPLE_DATA,
        risk_values=[0.0],
        budget=100.0,
        solver="pulp",
        excluded_players=[excluded],
        output_dir=output_dir,
    )

    metadata = json.loads((output_dir / "run_metadata.json").read_text())
    selected = pd.read_csv(output_dir / "selected_team_risk_0.csv")

    assert metadata["excluded_players"] == [excluded]
    assert metadata["input_rows_after_exclusion"] == (
        metadata["input_rows_before_exclusion"] - 1
    )
    assert excluded not in set(selected["Player Name"])

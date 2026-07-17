"""Run the paper-style risk-aversion experiments on a supplied dataset.

The default input is synthetic demonstration data. Exact reproduction of the
published numerical results requires the verified original research dataset.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import platform
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

from src.dream11_optimizer import OptimisationConfig, optimise_team


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Run Dream11 team selection across risk-aversion values."
    )
    parser.add_argument(
        "--input",
        type=Path,
        default=Path("data/example_players.csv"),
        help="Player CSV (default: data/example_players.csv)",
    )
    parser.add_argument(
        "--risk-values",
        type=float,
        nargs="+",
        default=[0.0, 0.5, 1.0, 2.0, 5.0, 10.0],
        help="Risk-aversion values to evaluate",
    )
    parser.add_argument("--budget", type=float, default=100.0)
    parser.add_argument(
        "--solver", choices=["auto", "gurobi", "pulp"], default="pulp"
    )
    parser.add_argument(
        "--exclude-player",
        action="append",
        default=[],
        help="Player to remove before optimisation; may be supplied more than once",
    )
    parser.add_argument(
        "--output-dir", type=Path, default=Path("outputs/paper_experiments")
    )
    return parser.parse_args()


def file_sha256(path: Path) -> str:
    """Return a stable fingerprint for the exact input file used in a run."""

    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(65536), b""):
            digest.update(chunk)
    return digest.hexdigest()


def summarise_team(team: pd.DataFrame, risk_aversion: float) -> dict[str, object]:
    captain = team.loc[team["Fantasy Role"] == "CAPTAIN", "Player Name"].iloc[0]
    vice_captain = team.loc[
        team["Fantasy Role"] == "VICE_CAPTAIN", "Player Name"
    ].iloc[0]
    type_counts = team["Player Type"].value_counts().sort_index()
    team_counts = team["Team"].value_counts().sort_index()
    return {
        "risk_aversion": risk_aversion,
        "captain": captain,
        "vice_captain": vice_captain,
        "credits_used": float(team["Price"].sum()),
        "expected_score_with_multipliers": float(
            (team["Expected Score"] * team["Score Multiplier"]).sum()
        ),
        "total_score_risk": float(team["Score Risk"].sum()),
        "risk_adjusted_objective": float(
            team["Risk-adjusted Contribution"].sum()
        ),
        "player_type_counts": "; ".join(
            f"{name}:{int(count)}" for name, count in type_counts.items()
        ),
        "real_team_counts": "; ".join(
            f"{name}:{int(count)}" for name, count in team_counts.items()
        ),
        "selected_players": "; ".join(team["Player Name"].tolist()),
    }


def create_figures(summary: pd.DataFrame, output_dir: Path) -> list[str]:
    """Create publication-friendly plots showing the score-risk trade-off."""

    figures = []

    fig, ax = plt.subplots()
    ax.plot(
        summary["risk_aversion"],
        summary["expected_score_with_multipliers"],
        marker="o",
    )
    ax.set_xlabel("Risk-aversion coefficient")
    ax.set_ylabel("Expected fantasy score")
    ax.set_title("Expected score versus risk aversion")
    ax.grid(True, alpha=0.3)
    fig.tight_layout()
    filename = "expected_score_vs_risk_aversion.png"
    fig.savefig(output_dir / filename, dpi=160)
    plt.close(fig)
    figures.append(filename)

    fig, ax = plt.subplots()
    ax.plot(
        summary["risk_aversion"],
        summary["total_score_risk"],
        marker="o",
    )
    ax.set_xlabel("Risk-aversion coefficient")
    ax.set_ylabel("Total selected-player score risk")
    ax.set_title("Selected-team risk versus risk aversion")
    ax.grid(True, alpha=0.3)
    fig.tight_layout()
    filename = "team_risk_vs_risk_aversion.png"
    fig.savefig(output_dir / filename, dpi=160)
    plt.close(fig)
    figures.append(filename)

    return figures


def run_experiments(
    input_path: Path,
    risk_values: list[float],
    budget: float,
    solver: str,
    excluded_players: list[str],
    output_dir: Path,
) -> pd.DataFrame:
    """Execute the experiment workflow and return its summary table."""

    if not input_path.exists():
        raise ValueError(f"Input file not found: {input_path}")
    if len(set(risk_values)) != len(risk_values):
        raise ValueError("Risk-aversion values must be unique")
    if any(value < 0 for value in risk_values):
        raise ValueError("Risk-aversion values must be non-negative")

    players = pd.read_csv(input_path)
    original_player_count = len(players)
    if excluded_players:
        requested = set(excluded_players)
        available = set(players["Player Name"])
        missing = sorted(requested - available)
        if missing:
            raise ValueError(f"Excluded player not present: {', '.join(missing)}")
        players = players.loc[~players["Player Name"].isin(requested)].copy()

    output_dir.mkdir(parents=True, exist_ok=True)
    summaries: list[dict[str, object]] = []
    selected_team_files = []

    for risk_value in risk_values:
        config = OptimisationConfig(
            risk_aversion=risk_value,
            budget=budget,
            solver=solver,
        )
        team = optimise_team(players, config)
        label = format(risk_value, "g").replace(".", "_")
        filename = f"selected_team_risk_{label}.csv"
        team.to_csv(output_dir / filename, index=False)
        selected_team_files.append(filename)
        summaries.append(summarise_team(team, risk_value))

    summary = pd.DataFrame(summaries)
    summary.to_csv(output_dir / "experiment_summary.csv", index=False)
    figure_files = create_figures(summary, output_dir)

    metadata = {
        "input": str(input_path),
        "input_sha256": file_sha256(input_path),
        "input_rows_before_exclusion": original_player_count,
        "input_rows_after_exclusion": len(players),
        "solver": solver,
        "budget": budget,
        "risk_values": risk_values,
        "excluded_players": excluded_players,
        "python_version": platform.python_version(),
        "pandas_version": pd.__version__,
        "numpy_version": np.__version__,
        "matplotlib_version": matplotlib.__version__,
        "generated_files": [
            "experiment_summary.csv",
            "run_metadata.json",
            *selected_team_files,
            *figure_files,
        ],
        "data_warning": (
            "Exact paper reproduction requires the verified original research dataset."
        ),
    }
    (output_dir / "run_metadata.json").write_text(
        json.dumps(metadata, indent=2), encoding="utf-8"
    )
    return summary


def main() -> None:
    args = parse_args()
    try:
        summary = run_experiments(
            input_path=args.input,
            risk_values=args.risk_values,
            budget=args.budget,
            solver=args.solver,
            excluded_players=args.exclude_player,
            output_dir=args.output_dir,
        )
    except ValueError as exc:
        raise SystemExit(str(exc)) from exc

    print(summary.to_string(index=False))
    print(f"\nResults written to {args.output_dir}")


if __name__ == "__main__":
    main()

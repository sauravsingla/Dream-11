"""Run the paper-style risk-aversion experiments on a supplied dataset.

The default input is synthetic demonstration data. Exact reproduction of the
published numerical results requires the verified original research dataset.
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path

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


def summarise_team(team: pd.DataFrame, risk_aversion: float) -> dict[str, object]:
    captain = team.loc[team["Fantasy Role"] == "CAPTAIN", "Player Name"].iloc[0]
    vice_captain = team.loc[
        team["Fantasy Role"] == "VICE_CAPTAIN", "Player Name"
    ].iloc[0]
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
        "selected_players": "; ".join(team["Player Name"].tolist()),
    }


def main() -> None:
    args = parse_args()
    if not args.input.exists():
        raise SystemExit(f"Input file not found: {args.input}")

    players = pd.read_csv(args.input)
    if args.exclude_player:
        requested = set(args.exclude_player)
        available = set(players["Player Name"])
        missing = sorted(requested - available)
        if missing:
            raise SystemExit(f"Excluded player not present: {', '.join(missing)}")
        players = players.loc[~players["Player Name"].isin(requested)].copy()

    args.output_dir.mkdir(parents=True, exist_ok=True)
    summaries: list[dict[str, object]] = []

    for risk_value in args.risk_values:
        config = OptimisationConfig(
            risk_aversion=risk_value,
            budget=args.budget,
            solver=args.solver,
        )
        team = optimise_team(players, config)
        label = str(risk_value).replace(".", "_")
        team.to_csv(args.output_dir / f"selected_team_risk_{label}.csv", index=False)
        summaries.append(summarise_team(team, risk_value))

    summary = pd.DataFrame(summaries)
    summary.to_csv(args.output_dir / "experiment_summary.csv", index=False)

    metadata = {
        "input": str(args.input),
        "solver": args.solver,
        "budget": args.budget,
        "risk_values": args.risk_values,
        "excluded_players": args.exclude_player,
        "data_warning": (
            "Exact paper reproduction requires the verified original research dataset."
        ),
    }
    (args.output_dir / "run_metadata.json").write_text(
        json.dumps(metadata, indent=2), encoding="utf-8"
    )

    print(summary.to_string(index=False))
    print(f"\nResults written to {args.output_dir}")


if __name__ == "__main__":
    main()

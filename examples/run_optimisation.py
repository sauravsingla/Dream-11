"""Run the paper-aligned Dream11 optimiser from the command line."""

from __future__ import annotations

import argparse
from pathlib import Path

import pandas as pd

from src.dream11_optimizer import OptimisationConfig, optimise_team


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Select a Dream11 team using the integer-optimisation model."
    )
    parser.add_argument("input_csv", type=Path, help="CSV containing candidate players")
    parser.add_argument(
        "--risk-aversion",
        type=float,
        default=0.0,
        help="Penalty applied to player score variability (default: 0.0)",
    )
    parser.add_argument(
        "--budget",
        type=float,
        default=100.0,
        help="Maximum available fantasy credits (default: 100)",
    )
    parser.add_argument(
        "--output",
        type=Path,
        help="Optional path for saving the selected team as CSV",
    )
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    if not args.input_csv.exists():
        raise SystemExit(f"Input file not found: {args.input_csv}")

    players = pd.read_csv(args.input_csv)
    config = OptimisationConfig(
        risk_aversion=args.risk_aversion,
        budget=args.budget,
    )
    selected = optimise_team(players, config)

    columns = [
        "Player Name",
        "Player Type",
        "Team",
        "Price",
        "Fantasy Role",
        "Expected Score",
        "Score Risk",
        "Risk-adjusted Contribution",
    ]
    print(selected[columns].to_string(index=False))

    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        selected.to_csv(args.output, index=False)
        print(f"\nSaved selected team to {args.output}")


if __name__ == "__main__":
    main()

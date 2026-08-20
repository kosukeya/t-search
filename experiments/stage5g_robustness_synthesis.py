"""Print Stage 5G robustness summaries for the declared control families."""

from __future__ import annotations

from dataclasses import asdict

from t_search.stage5_robustness import (
    global_phase_density_residuals,
    stage5_joint_robustness_summary,
)


def print_summary(label: str, **kwargs) -> None:
    summary = stage5_joint_robustness_summary(**kwargs)
    print(f"\n[{label}]")
    for key, value in asdict(summary).items():
        print(f"{key}: {value}")


def main() -> None:
    print_summary("canonical d=3 / generic", dimension=3, coefficient_family="generic")
    print_summary("canonical d=3 / alternating", dimension=3, coefficient_family="alternating")
    print_summary("canonical d=3 / sparse", dimension=3, coefficient_family="sparse")
    print_summary("symmetric d=5 / generic", dimension=5, coefficient_family="generic")
    print_summary("symmetric d=5 / sparse", dimension=5, coefficient_family="sparse")
    print_summary(
        "asymmetric qutrit rates (1,1,2) / generic",
        dimension=3,
        rates=(1.0, 1.0, 2.0),
        coefficient_family="generic",
    )
    print_summary(
        "asymmetric qutrit rates (1,1,2) / alternating",
        dimension=3,
        rates=(1.0, 1.0, 2.0),
        coefficient_family="alternating",
    )

    for label, dimension, rates in (
        ("canonical d=3", 3, (1.0, 1.0, 1.0)),
        ("symmetric d=5", 5, (1.0, 1.0, 1.0)),
        ("asymmetric qutrit", 3, (1.0, 1.0, 2.0)),
    ):
        density, probability = global_phase_density_residuals(
            dimension, rates=rates, phase=0.731
        )
        print(f"\n[{label} global phase]")
        print(f"max_density_residual: {density}")
        print(f"max_clock_probability_residual: {probability}")


if __name__ == "__main__":
    main()

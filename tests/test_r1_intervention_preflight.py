"""Check the feasibility boundary through the published audit entry point."""

from pathlib import Path
import runpy


def test_r1_existing_history_audit():
    root = Path(__file__).resolve().parents[1]
    namespace = runpy.run_path(str(root / "experiments/r1_intervention_preflight.py"))
    namespace["audit"]()  # Checks support leakage, TP, metrics and all matrix units.

"""Verify the boundary comparison using the ordinary CI import environment."""
from pathlib import Path
import runpy


def test_r_boundary_supplement():
    root = Path(__file__).resolve().parents[1]
    runpy.run_path(str(root / "experiments/r_boundary_supplement.py"))["audit"]()

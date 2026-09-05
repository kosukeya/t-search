"""Run the finite device audit in the ordinary installed package environment."""
from pathlib import Path
import runpy


def test_r1b_readout_design_audit():
    root = Path(__file__).resolve().parents[1]
    runpy.run_path(str(root / "experiments/r1b_readout_design_audit.py"))["audit"]()

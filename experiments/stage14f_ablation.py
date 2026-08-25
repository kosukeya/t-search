"""Run the Stage 14F executable control snapshot."""

from __future__ import annotations

from dataclasses import asdict
import json

from t_search.stage14_ablation import stage14f_diagnostics, stage14f_summary


def main() -> None:
    diagnostics = stage14f_diagnostics()
    payload = {
        **asdict(diagnostics),
        **stage14f_summary(),
    }
    print(json.dumps(payload, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()

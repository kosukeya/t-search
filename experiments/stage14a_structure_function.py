"""Run the frozen Stage 14A carrier diagnostics."""

from __future__ import annotations

from dataclasses import asdict
import json

from t_search.stage14_structure_function import stage14a_diagnostics


def main() -> None:
    print(json.dumps(asdict(stage14a_diagnostics()), indent=2, sort_keys=True))


if __name__ == "__main__":
    main()

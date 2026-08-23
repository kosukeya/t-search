"""Executable Stage 12C typed gauge-atlas / quotient checkpoint."""

from __future__ import annotations

import json

from t_search.stage12_gauge_atlas import stage12c_summary


def main() -> None:
    print(json.dumps(stage12c_summary(), indent=2, sort_keys=True))


if __name__ == "__main__":
    main()

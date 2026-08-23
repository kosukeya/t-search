"""Executable Stage 12D checkpoint."""

from __future__ import annotations

from pprint import pprint

from t_search.stage12_measurement import stage12d_summary


def main() -> None:
    pprint(stage12d_summary())


if __name__ == "__main__":
    main()

"""Run the Stage 13E executable diagnostic snapshot."""

from __future__ import annotations

import json

from t_search.stage13_measurement import stage13e_summary


def main() -> None:
    print(json.dumps(stage13e_summary(), indent=2, sort_keys=True))


if __name__ == "__main__":
    main()

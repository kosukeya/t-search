"""Print Stage 7A spectator-memory diagnostics as JSON."""

from __future__ import annotations

import json

from t_search.stage7_spectator import stage7a_summary


def main() -> None:
    print(json.dumps(stage7a_summary(), indent=2, sort_keys=True))


if __name__ == "__main__":
    main()

"""Print Stage 7C relational-history diagnostics as JSON."""

from __future__ import annotations

import json

from t_search.stage7_history import stage7c_summary


def main() -> None:
    print(json.dumps(stage7c_summary(), indent=2, sort_keys=True))


if __name__ == "__main__":
    main()

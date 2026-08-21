"""Print Stage 7B reversible target-specific record diagnostics as JSON."""

from __future__ import annotations

import json

from t_search.stage7_record import stage7b_summary


def main() -> None:
    print(json.dumps(stage7b_summary(), indent=2, sort_keys=True))


if __name__ == "__main__":
    main()

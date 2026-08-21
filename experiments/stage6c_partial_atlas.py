"""Print Stage 6C partial-atlas diagnostics as JSON."""

from __future__ import annotations

import json

from t_search.stage6_partial_atlas import stage6c_summary_rows


def main() -> None:
    print(json.dumps(stage6c_summary_rows(), indent=2, sort_keys=True))


if __name__ == "__main__":
    main()

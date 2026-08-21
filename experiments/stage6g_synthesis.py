"""Print Stage 6G synthesis and Stage 7 gate diagnostics as JSON."""

from __future__ import annotations

import json

from t_search.stage6_synthesis import stage6g_rows


def main() -> None:
    print(json.dumps(stage6g_rows(), indent=2, sort_keys=True))


if __name__ == "__main__":
    main()

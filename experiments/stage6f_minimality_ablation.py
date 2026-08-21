"""Print Stage 6F minimality / ablation diagnostics as JSON."""

from __future__ import annotations

import json

from t_search.stage6_ablation import stage6f_rows


def main() -> None:
    print(json.dumps(stage6f_rows(), indent=2, sort_keys=True))


if __name__ == "__main__":
    main()

"""Print the Stage 7G synthesis, exit audit, and Stage 8 gate ranking as JSON."""

from __future__ import annotations

import json

from t_search.stage7_synthesis import stage7g_rows


if __name__ == "__main__":
    print(json.dumps(stage7g_rows(), indent=2, sort_keys=True))

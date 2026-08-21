"""Executable Stage 7F ablation / reconstruction / mismatch checkpoint."""

from __future__ import annotations

import json

from t_search.stage7_ablation import stage7f_summary


if __name__ == "__main__":
    print(json.dumps(stage7f_summary(), indent=2, sort_keys=True))

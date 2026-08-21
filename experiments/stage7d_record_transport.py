"""Executable Stage 7D record-transport checkpoint."""

from __future__ import annotations

import json

from t_search.stage7_record_transport import stage7d_summary


if __name__ == "__main__":
    print(json.dumps(stage7d_summary(), indent=2, sort_keys=True))

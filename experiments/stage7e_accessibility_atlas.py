"""Executable Stage 7E accessibility/partial-atlas checkpoint."""

from __future__ import annotations

import json

from t_search.stage7_accessibility_atlas import stage7e_summary


if __name__ == "__main__":
    print(json.dumps(stage7e_summary(), indent=2, sort_keys=True))

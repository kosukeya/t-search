"""Run the Stage 14G executable synthesis and print a JSON-friendly summary."""

from __future__ import annotations

import json

from t_search.stage14_synthesis import stage14g_summary


if __name__ == "__main__":
    print(json.dumps(stage14g_summary(), indent=2))

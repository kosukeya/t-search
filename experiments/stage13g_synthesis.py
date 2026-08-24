"""Run the Stage 13G executable synthesis and print a JSON-friendly summary."""

from __future__ import annotations

import json

from t_search.stage13_synthesis import stage13g_summary


def _default(value):
    if hasattr(value, "value"):
        return value.value
    if hasattr(value, "as_dict"):
        return value.as_dict()
    if hasattr(value, "__dict__"):
        return value.__dict__
    return str(value)


if __name__ == "__main__":
    print(json.dumps(stage13g_summary(), indent=2, default=_default))

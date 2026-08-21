"""Print Stage 8B typed quantum modal diagnostics as JSON."""

from __future__ import annotations

import json

from t_search.stage8_modal import stage8b_summary


def main() -> None:
    print(json.dumps(stage8b_summary(), indent=2, sort_keys=True))


if __name__ == "__main__":
    main()

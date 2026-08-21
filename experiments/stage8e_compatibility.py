"""Print Stage 8E P/O/R/V compatibility diagnostics as JSON."""

from __future__ import annotations

import json

from t_search.stage8_compatibility import stage8e_summary


def main() -> None:
    print(json.dumps(stage8e_summary(), indent=2, sort_keys=True))


if __name__ == "__main__":
    main()

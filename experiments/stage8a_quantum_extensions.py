"""Print Stage 8A common quantum-extension diagnostics as JSON."""

from __future__ import annotations

import json

from t_search.stage8_continuations import stage8a_summary


def main() -> None:
    print(json.dumps(stage8a_summary(), indent=2, sort_keys=True))


if __name__ == "__main__":
    main()

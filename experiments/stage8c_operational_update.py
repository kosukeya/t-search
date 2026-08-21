"""Print Stage 8C operational/update diagnostics as JSON."""

from __future__ import annotations

import json

from t_search.stage8_operational import stage8c_summary


def main() -> None:
    print(json.dumps(stage8c_summary(), indent=2, sort_keys=True))


if __name__ == "__main__":
    main()

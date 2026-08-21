"""Print the executable Stage 6A W1--W5 witness inventory as JSON."""

from __future__ import annotations

import json

from t_search.stage6_inventory import stage6a_inventory_rows


def main() -> None:
    print(json.dumps(stage6a_inventory_rows(), indent=2, sort_keys=True))


if __name__ == "__main__":
    main()

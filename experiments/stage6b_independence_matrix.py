"""Print Stage 6B evidence cases and implication matrix as JSON."""

from __future__ import annotations

import json

from t_search.stage6_independence import stage6b_case_rows, stage6b_matrix_rows


def main() -> None:
    payload = {
        "cases": stage6b_case_rows(),
        "matrix": stage6b_matrix_rows(),
    }
    print(json.dumps(payload, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()

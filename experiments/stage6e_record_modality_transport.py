"""Print Stage 6E record/modality transport diagnostics as JSON."""

from __future__ import annotations

import json

from t_search.stage6_record_modality import stage6e_rows


def main() -> None:
    print(json.dumps(stage6e_rows(), indent=2, sort_keys=True))


if __name__ == "__main__":
    main()

"""Print Stage 8D continuation-aware modal transport diagnostics as JSON."""

from __future__ import annotations

import json

from t_search.stage8_modal_transport import stage8d_summary


def main() -> None:
    print(json.dumps(stage8d_summary(), indent=2, sort_keys=True))


if __name__ == "__main__":
    main()

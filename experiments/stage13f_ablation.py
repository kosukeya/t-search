from __future__ import annotations

from dataclasses import asdict
import json

from t_search.stage13_ablation import stage13f_diagnostics, stage13f_summary


def main() -> None:
    payload = {
        "diagnostics": asdict(stage13f_diagnostics()),
        "summary": stage13f_summary(),
    }
    print(json.dumps(payload, indent=2, default=str))


if __name__ == "__main__":
    main()

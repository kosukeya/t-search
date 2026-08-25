"""Run the Stage 14E executable diagnostic snapshot."""
from __future__ import annotations
import json
from t_search.stage14_measurement import stage14e_summary

def main() -> None:
    print(json.dumps(stage14e_summary(), indent=2, sort_keys=True))

if __name__ == "__main__":
    main()

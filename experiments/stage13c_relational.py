from __future__ import annotations

from dataclasses import asdict
from pprint import pprint

from t_search.stage13_relational import stage13c_diagnostics


if __name__ == "__main__":
    pprint(asdict(stage13c_diagnostics()))

from __future__ import annotations

from dataclasses import asdict
from pprint import pprint

from t_search.stage13_gauge_atlas import stage13d_diagnostics


if __name__ == "__main__":
    pprint(asdict(stage13d_diagnostics()))

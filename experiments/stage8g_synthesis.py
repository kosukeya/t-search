"""Print the Stage 8G synthesis, pre-merge audit, and selected Stage 9 gate."""

from pprint import pprint

from t_search.stage8_exit_audit import stage8_pre_merge_audit
from t_search.stage8_synthesis import stage8g_summary


if __name__ == "__main__":
    pprint(stage8g_summary())
    pprint(stage8_pre_merge_audit().as_dict())

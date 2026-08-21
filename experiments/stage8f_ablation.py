import json
from t_search.stage8_ablation import stage8f_summary

print(json.dumps(stage8f_summary(), indent=2, default=str))

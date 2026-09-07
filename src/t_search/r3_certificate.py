"""Two-basis certificate: probabilities and declared assumptions only.

No channel, state, experiment label, reference fidelity, or I/O dependencies.
Assumption flags are declarations, not independent physical validations.
"""
import math
from numbers import Real

PROBABILITY_KEYS = ("z0", "z1", "x_plus", "x_minus")
ASSUMPTION_KEYS = (
    "trusted_preparation", "trusted_measurement", "qubit_input_output",
    "same_cptp_process", "reset_between_trials", "no_input_or_setting_leakage",
    "no_postselection", "exact_probabilities",
)
NUMERICAL_MARGIN = 1e-10


def certify(probabilities, assumptions):
    """Hofmann bound for a fixed qubit channel with identity as target.

    Values are Born probabilities, not finite-shot frequency estimates. Reject
    out-of-range data rather than clipping it. The physical lower bound max(0,L)
    is part of the theorem. A numerical guard only withholds borderline claims.
    """
    if set(probabilities) != set(PROBABILITY_KEYS):
        raise ValueError("Supply exactly four named correctness probabilities")
    if set(assumptions) != set(ASSUMPTION_KEYS):
        raise ValueError("Supply exactly the declared trust/connection assumptions")
    if any(assumptions[k] is not True for k in ASSUMPTION_KEYS):
        raise ValueError("Certificate unavailable when an assumption is not affirmed")
    p = {}
    for key in PROBABILITY_KEYS:
        value = probabilities[key]
        if isinstance(value, bool) or not isinstance(value, Real):
            raise ValueError("Probabilities must be real numbers, not flags")
        value = float(value)
        if not math.isfinite(value) or not 0 <= value <= 1:
            raise ValueError("Probabilities must be finite and lie in [0,1]")
        p[key] = value
    fz = (p["z0"]+p["z1"])/2
    fx = (p["x_plus"]+p["x_minus"])/2
    lower, upper = max(0., fz+fx-1), min(fz, fx)
    certified = lower > .5+NUMERICAL_MARGIN
    return {"F_Z": fz, "F_X": fx, "lower_bound": lower, "upper_bound": upper,
            "non_measure_prepare_certified": certified,
            "decision": "certified_under_declared_assumptions" if certified else "inconclusive",
            "numerical_margin": NUMERICAL_MARGIN,
            "target": "identity channel; normalized Bell overlap without square root",
            "scope": "implemented channel only; not optimal recovery or gate identification",
            "assumptions_status": "declared, not validated by this function"}

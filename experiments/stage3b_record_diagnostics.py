"""Stage 3B exact record-diagnostic experiment.

This script reports measurement outputs only.  Position labels remain neutral and
no temporal-arrow interpretation is made here.
"""

from t_search.stage3 import canonical_forward_ensemble
from t_search.stage3_diagnostics import (
    accessibility_arrow_score,
    accessibility_profile,
    component_conditional_entropy,
    component_decoding_accuracy,
    component_entropy,
    component_mutual_information,
    record_arrow_score,
    record_profile,
)


def main() -> None:
    ensemble = canonical_forward_ensemble()

    print("Stage 3B — exact record diagnostics")
    print("neutral current position: 1")
    print("record register: M_1")
    print("target variable: X_j")
    print()

    print("Subsystem entropies")
    print(f"H(M_0) = {component_entropy(ensemble, 0, 'm'):.6f} bits")
    print(f"H(M_1) = {component_entropy(ensemble, 1, 'm'):.6f} bits")
    print(f"H(X_0) = {component_entropy(ensemble, 0, 'x'):.6f} bits")
    print(f"H(X_2) = {component_entropy(ensemble, 2, 'x'):.6f} bits")
    print()

    print("Mutual information")
    print(
        "I(M_1; X_0) = "
        f"{component_mutual_information(ensemble, 1, 'm', 0, 'x'):.6f} bits"
    )
    print(
        "I(M_1; X_2) = "
        f"{component_mutual_information(ensemble, 1, 'm', 2, 'x'):.6f} bits"
    )
    print()

    print("Conditional entropy")
    print(
        "H(X_0 | M_1) = "
        f"{component_conditional_entropy(ensemble, 0, 'x', 1, 'm'):.6f} bits"
    )
    print(
        "H(X_2 | M_1) = "
        f"{component_conditional_entropy(ensemble, 2, 'x', 1, 'm'):.6f} bits"
    )
    print()

    print("Bayes-optimal accessibility")
    print(
        "Acc(M_1 -> X_0) = "
        f"{component_decoding_accuracy(ensemble, 1, 'm', 0, 'x'):.6f}"
    )
    print(
        "Acc(M_1 -> X_2) = "
        f"{component_decoding_accuracy(ensemble, 1, 'm', 2, 'x'):.6f}"
    )
    print()

    print(f"Q_R(1,j) = {record_profile(ensemble)}")
    print(f"Acc profile = {accessibility_profile(ensemble)}")
    print(f"A_R(1,1) = {record_arrow_score(ensemble):.6f} bits")
    print(f"A_Acc(1,1) = {accessibility_arrow_score(ensemble):.6f}")
    print()
    print("Interpretive guard: these are signed neutral-side contrasts, not yet a temporal-arrow claim.")


if __name__ == "__main__":
    main()

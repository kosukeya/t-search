"""Run the Stage 3F accessibility/information controls."""

from fractions import Fraction

from t_search.stage3_accessibility import (
    LocalAccessPolicy,
    compatible_history_count,
    local_observation_decoding_accuracy,
    local_observation_mutual_information,
    make_local_observation_ensemble,
    posterior_histories_given_outcome,
    record_readout_accessibility_arrow_score,
    record_readout_arrow_score,
    record_readout_decoding_accuracy,
    record_readout_mutual_information,
)
from t_search.stage3_diagnostics import component_mutual_information
from t_search.stage3_local import canonical_record_block


def main() -> None:
    block = canonical_record_block()
    global_record_information = component_mutual_information(
        block.ensemble, 1, "m", 0, "x"
    )

    print("Stage 3F — accessibility and information controls")
    print("guard: inaccessible information != ontologically absent information")
    print(f"global true-register I(M_1;X_0)={global_record_information:.12f}")
    print()

    for epsilon in (Fraction(0, 1), Fraction(1, 4), Fraction(1, 2)):
        observations = make_local_observation_ensemble(
            block,
            LocalAccessPolicy(
                expose_x=False,
                expose_m=True,
                record_error_probability=epsilon,
            ),
        )
        print(f"record-only epsilon={float(epsilon):.2f}")
        print(
            "  I(M_obs;X_0)=",
            f"{record_readout_mutual_information(observations, target_position=0):.12f}",
        )
        print(
            "  I(M_obs;X_2)=",
            f"{record_readout_mutual_information(observations, target_position=2):.12f}",
        )
        print(
            "  Acc(M_obs->X_0)=",
            f"{record_readout_decoding_accuracy(observations, target_position=0):.12f}",
        )
        print(
            "  A_R_access=",
            f"{record_readout_arrow_score(observations):.12f}",
        )
        print(
            "  A_Acc_access=",
            f"{record_readout_accessibility_arrow_score(observations):.12f}",
        )

    maximally_noisy_full = make_local_observation_ensemble(
        block,
        LocalAccessPolicy(
            expose_x=True,
            expose_m=True,
            record_error_probability=Fraction(1, 2),
        ),
    )
    print()
    print("redundant X+M interface at epsilon=0.5")
    print(
        "  record-only I(M_obs;X_0)=",
        f"{record_readout_mutual_information(maximally_noisy_full, target_position=0):.12f}",
    )
    print(
        "  full-local I((X_1,M_obs);X_0)=",
        f"{local_observation_mutual_information(maximally_noisy_full, target_position=0):.12f}",
    )
    print(
        "  full-local Acc((X_1,M_obs)->X_0)=",
        f"{local_observation_decoding_accuracy(maximally_noisy_full, target_position=0):.12f}",
    )

    masked_x_noisy = make_local_observation_ensemble(
        block,
        LocalAccessPolicy(
            expose_x=False,
            expose_m=True,
            record_error_probability=Fraction(1, 4),
        ),
    )
    outcome = (None, 1)
    posterior = posterior_histories_given_outcome(masked_x_noisy, outcome)
    print()
    print("masked-X noisy outcome (None,1)")
    print("  compatible histories=", compatible_history_count(masked_x_noisy, outcome))
    for trajectory, probability in posterior:
        print(" ", trajectory, probability)

    print()
    print("guard: readout noise changes the interface, not the global reversible block")


if __name__ == "__main__":
    main()

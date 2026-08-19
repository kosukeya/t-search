"""Stage 3E checkpoint experiment: explicit local projection and typed Potentiality."""

from t_search.stage2_epistemic import canonical_epistemic_model, project_epistemic_view
from t_search.stage2_ontic import canonical_ontic_model, project_ontic_view
from t_search.stage3 import Microstate
from t_search.stage3_local import (
    canonical_record_block,
    combine_with_epistemic_potentiality,
    combine_with_ontic_potentiality,
    compatible_global_histories,
    project_record_view,
    reconstruct_global_history,
)


def main() -> None:
    block = canonical_record_block()
    trajectory = next(
        t for t in block.ensemble.trajectories if t[0] == Microstate(1, 0, 1)
    )

    central = project_record_view(block, trajectory, position=1)
    upper = project_record_view(block, trajectory, position=2)
    single_compatible = compatible_global_histories(block, (central,))
    reconstructed = reconstruct_global_history(block, (central, upper))

    epistemic = combine_with_epistemic_potentiality(
        central,
        project_epistemic_view(canonical_epistemic_model(), ("p", "n")),
    )
    ontic = combine_with_ontic_potentiality(
        central,
        project_ontic_view(canonical_ontic_model()),
    )

    print("Stage 3E — complete local view")
    print(f"global trajectory: {trajectory}")
    print(f"central local actuality (X,M): {central.actuality}")
    print(f"central record value: {central.records.register_value}")
    print(f"central orientation: {central.records.orientation}")
    print(f"compatible global histories from central view: {len(single_compatible)}")
    print(f"two-view family reconstructs original: {reconstructed == trajectory}")
    print(f"epistemic potentiality type: {type(epistemic.potentiality).__name__}")
    print(f"ontic potentiality type: {type(ontic.potentiality).__name__}")
    print(f"shared record layer: {epistemic.records == ontic.records}")
    print("product construction != claim of one unified physical substrate")


if __name__ == "__main__":
    main()

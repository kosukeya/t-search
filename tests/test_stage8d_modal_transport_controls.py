import numpy as np

from t_search.stage8_modal import (
    canonical_stage8b_models,
    make_ontic_quantum_extension_model,
)
from t_search.stage8_modal_transport import (
    modal_event_correspondence,
    perspective_modal_view,
    stage8d_transport_diagnostics,
)

ATOL = 1e-9


def _density(view):
    return np.asarray(view.predictive_density, dtype=np.complex128)


def test_stage8d_non_a_charts_do_not_preserve_the_stage8a_shared_current_pure_ray():
    diagnostics = stage8d_transport_diagnostics()

    # A/e1 is the frozen Stage 8A common-current anchor.
    assert diagnostics.a_e1_shared_current_density_residual <= ATOL

    # In the genuine B/C conditional charts, h_L and h_R no longer appear as
    # the same normalized local pure ray. This is a measured limitation of the
    # canonical continuation family, not a failure of the per-continuation maps.
    assert diagnostics.min_non_a_same_reading_density_residual > 0.5
    assert diagnostics.max_non_a_same_reading_density_residual > 1.0


def test_stage8d_weight_mismatch_remains_detectable_after_genuine_clock_change():
    epistemic, _ = canonical_stage8b_models(selected_id="h_L")
    mismatch = make_ontic_quantum_extension_model(
        epistemic.carrier,
        (0.75, 0.25),
    )
    chi = modal_event_correspondence(epistemic.carrier, "preserving")

    residuals = []
    for clock in ("B", "C"):
        for index in range(3):
            matched = perspective_modal_view(
                epistemic, clock, index, correspondence=chi
            )
            changed = perspective_modal_view(
                mismatch, clock, index, correspondence=chi
            )
            residuals.append(float(np.linalg.norm(_density(matched) - _density(changed))))

    assert max(residuals) > 0.1

import numpy as np

from t_search.stage5_clock_change import DEFAULT_ATOL
from t_search.stage7_history import CURRENT_EVENT, UPPER_EVENT
from t_search.stage9_modal import (
    FUTURE_SIGNATURE_LEFT,
    FUTURE_SIGNATURE_OTHER,
    canonical_stage9_directional_carrier,
    canonical_stage9_future_signature_measurement,
    continuation_future_signature_probabilities,
)
from t_search.stage10_reference import (
    STAGE10_REFERENCE_BASIS,
    STAGE10_REFERENCE_CLOCK,
    STAGE10_REFERENCE_FAMILY_ID,
    STAGE10_REFERENCE_NORMALIZATION,
    canonical_stage10_reference_measurement_family,
    reference_effects_for_continuation,
    stage10_reference_probabilities,
    stage10_reference_schema_audit,
    stage10a_reference_diagnostics,
)


def test_stage10a_typed_reference_family_reproduces_stage9c_measurement() -> None:
    carrier = canonical_stage9_directional_carrier()
    stage9 = canonical_stage9_future_signature_measurement(carrier)
    family = canonical_stage10_reference_measurement_family()

    assert family.family_id == STAGE10_REFERENCE_FAMILY_ID
    assert family.clock == STAGE10_REFERENCE_CLOCK == "A"
    assert family.clock_index == UPPER_EVENT
    assert family.coordinate_basis == STAGE10_REFERENCE_BASIS
    assert family.normalization == STAGE10_REFERENCE_NORMALIZATION
    assert tuple(item.outcome_id for item in family.outcomes) == stage9.outcome_names
    assert stage9.outcome_names == (FUTURE_SIGNATURE_LEFT, FUTURE_SIGNATURE_OTHER)

    for continuation in carrier.continuations:
        typed = reference_effects_for_continuation(family, continuation.continuation_id)
        assert tuple(effect.outcome_id for effect in typed) == stage9.outcome_names
        for effect, reference in zip(typed, stage9.effects, strict=True):
            assert effect.family_id == family.family_id
            assert effect.continuation_id == continuation.continuation_id
            assert effect.coordinate_basis == family.coordinate_basis
            assert effect.normalization == family.normalization
            assert np.allclose(effect.matrix, reference, atol=DEFAULT_ATOL, rtol=0.0)


def test_stage10a_outcome_provenance_and_anchor_target_typing_are_explicit() -> None:
    family = canonical_stage10_reference_measurement_family()
    assert family.prediction_anchor == CURRENT_EVENT
    assert family.target_event == UPPER_EVENT
    assert family.prediction_anchor != family.target_event

    for outcome in family.outcomes:
        assert outcome.outcome_id
        assert outcome.semantics
        assert outcome.provenance
    for effect in family.effects:
        assert effect.prediction_anchor == CURRENT_EVENT
        assert effect.target_event == UPPER_EVENT
        assert effect.clock == "A"
        assert effect.clock_index == UPPER_EVENT
        assert effect.outcome_semantics
        assert effect.outcome_provenance
        assert effect.effect_provenance


def test_stage10a_reference_positivity_and_completeness_are_revalidated() -> None:
    family = canonical_stage10_reference_measurement_family()
    for continuation_id in family.continuation_ids:
        effects = reference_effects_for_continuation(family, continuation_id)
        matrices = tuple(effect.matrix for effect in effects)
        identity = np.eye(matrices[0].shape[0], dtype=np.complex128)
        assert np.linalg.norm(sum(matrices) - identity) <= DEFAULT_ATOL
        for matrix in matrices:
            assert np.linalg.norm(matrix - matrix.conj().T) <= DEFAULT_ATOL
            minimum = np.min(np.linalg.eigvalsh((matrix + matrix.conj().T) / 2.0))
            assert minimum >= -DEFAULT_ATOL


def test_stage10a_reference_family_remains_operationally_discriminating() -> None:
    carrier = canonical_stage9_directional_carrier()
    family = canonical_stage10_reference_measurement_family()
    vectors = []
    for continuation in carrier.continuations:
        probabilities = dict(stage10_reference_probabilities(family, continuation))
        vectors.append(
            np.asarray(
                [
                    probabilities[FUTURE_SIGNATURE_LEFT],
                    probabilities[FUTURE_SIGNATURE_OTHER],
                ],
                dtype=float,
            )
        )
    assert np.linalg.norm(vectors[0] - vectors[1]) > DEFAULT_ATOL
    diagnostics = stage10a_reference_diagnostics()
    assert diagnostics.future_branch_overlap_squared < 1.0 - DEFAULT_ATOL
    assert diagnostics.operationally_discriminating


def test_stage10a_per_continuation_probabilities_reproduce_stage9c_likelihoods() -> None:
    carrier = canonical_stage9_directional_carrier()
    family = canonical_stage10_reference_measurement_family()
    for continuation in carrier.continuations:
        stage10 = dict(stage10_reference_probabilities(family, continuation))
        stage9 = dict(continuation_future_signature_probabilities(carrier, continuation))
        assert set(stage10) == set(stage9)
        for outcome in stage10:
            assert abs(stage10[outcome] - stage9[outcome]) <= DEFAULT_ATOL
        assert abs(sum(stage10.values()) - 1.0) <= 10 * DEFAULT_ATOL


def test_stage10a_public_reference_schema_has_no_hidden_selector_or_modal_type() -> None:
    family = canonical_stage10_reference_measurement_family()
    public_fields, forbidden, selector_free = stage10_reference_schema_audit(family)
    assert selector_free
    assert forbidden == ()
    for forbidden_name in (
        "selected_continuation",
        "selected_continuation_id",
        "selector",
        "hidden_selector",
        "model_type",
        "modal_type",
        "semantic_type",
        "privileged_modal_type",
    ):
        assert forbidden_name not in public_fields


def test_stage10a_diagnostics_close_criteria_11_through_16() -> None:
    diagnostics = stage10a_reference_diagnostics()
    assert diagnostics.continuation_count == 2
    assert diagnostics.typed_effect_count == 4
    assert diagnostics.canonical_outcomes_reproduced
    assert diagnostics.canonical_effects_reproduced
    assert diagnostics.prediction_anchor_explicit
    assert diagnostics.target_event_explicit
    assert diagnostics.anchor_target_distinct
    assert diagnostics.max_effect_residual <= DEFAULT_ATOL
    assert diagnostics.max_completeness_residual <= DEFAULT_ATOL
    assert diagnostics.minimum_effect_eigenvalue >= -DEFAULT_ATOL
    assert diagnostics.operationally_discriminating
    assert diagnostics.max_stage9_probability_residual <= DEFAULT_ATOL
    assert diagnostics.all_reference_probabilities_normalized
    assert diagnostics.public_schema_selector_free

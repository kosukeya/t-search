from t_search.stage8_continuations import (
    canonical_continuation_left,
    canonical_continuation_right,
    renamed_continuation,
)
from t_search.stage8_modal import (
    make_epistemic_quantum_model,
    make_quantum_continuation_carrier,
    matched_uniform_weights,
)
from t_search.stage8_modal_transport import (
    ModalEventCorrespondence,
    audit_modal_correspondence,
    perspective_modal_view,
)


def test_stage8d_physical_class_correspondence_survives_representative_renaming():
    renamed_left = renamed_continuation(canonical_continuation_left(), "renamed-left")
    carrier = make_quantum_continuation_carrier(
        (renamed_left, canonical_continuation_right())
    )
    model = make_epistemic_quantum_model(
        carrier,
        renamed_left,
        matched_uniform_weights(carrier),
    )

    # IDs are display handles.  chi explicitly maps the renamed source
    # representative to the canonical physically equivalent target class.
    chi = ModalEventCorrespondence(
        name="preserving",
        source_current_event=carrier.current_anchor,
        target_current_event=carrier.current_anchor,
        declared_orientation="preserving",
        class_map=(("renamed-left", "h_L"), ("h_R", "h_R")),
    )
    audit = audit_modal_correspondence(carrier, chi)

    assert audit.bijective is True
    assert audit.current_event_preserved is True
    assert audit.physical_classes_preserved is True
    assert audit.valid is True

    view = perspective_modal_view(model, "B", 0, correspondence=chi)
    assert view.continuation_ids == ("h_L", "h_R")
    assert view.continuation_weights == (0.5, 0.5)

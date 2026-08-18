"""Stage 2E: compare epistemic and ontic updates under one observation.

This module does not add a new temporal dynamics mechanism. It applies the already
specified Stage 2B and Stage 2C update rules to the same explicit observation and
compares their ontology-neutral operational views before and after the update.

The comparison keeps privileged internal diagnostics separate from the operational
interface. In particular, preservation of the epistemic selected history is recorded
without inserting that datum into ``OperationalView``.
"""

from __future__ import annotations

from dataclasses import dataclass, fields

from .stage1 import EventId
from .stage2 import History, Prefix
from .stage2_epistemic import (
    EpistemicHistoryModel,
    condition_epistemic_model,
    project_epistemic_view,
    selected_history,
)
from .stage2_ontic import (
    OnticExtensionModel,
    project_ontic_view,
    update_ontic_model,
)
from .stage2_operational import (
    OperationalComparison,
    OperationalView,
    compare_operational_views,
    operationalize_epistemic_view,
    operationalize_ontic_view,
)


@dataclass(frozen=True)
class Stage2UpdateComparison:
    """Before/after operational comparison plus privileged update diagnostics."""

    observed_next: EventId
    epistemic_before: OperationalView
    ontic_before: OperationalView
    before_comparison: OperationalComparison
    epistemic_after: OperationalView
    ontic_after: OperationalView
    after_comparison: OperationalComparison
    epistemic_selected_history_before: History
    epistemic_selected_history_after: History
    epistemic_selected_history_preserved: bool
    updated_epistemic_model: EpistemicHistoryModel
    updated_epistemic_prefix: Prefix
    updated_ontic_model: OnticExtensionModel


def _selected_future_like_fields(model: object) -> tuple[str, ...]:
    """Return explicit selected-future-like dataclass field names, if any.

    This is a structural diagnostic only. It intentionally checks the model schema,
    not arbitrary runtime values, and is not part of the operational interface.
    """

    if not hasattr(model, "__dataclass_fields__"):
        return ()
    names = {field.name for field in fields(model)}
    candidates = {
        "selected_history",
        "hidden_history",
        "selected_future",
        "hidden_future",
    }
    return tuple(sorted(names & candidates))


def ontic_selected_future_fields(model: OnticExtensionModel) -> tuple[str, ...]:
    """Privileged structural diagnostic for explicit future-selector fields."""

    return _selected_future_like_fields(model)


def compare_common_observation(
    epistemic_model: EpistemicHistoryModel,
    epistemic_prefix: Prefix,
    ontic_model: OnticExtensionModel,
    observed_next: EventId,
) -> Stage2UpdateComparison:
    """Apply one explicit observation to both Stage 2 model families.

    Preconditions deliberately require the same current Actuality/prefix. The two
    model families may differ internally, but Stage 2E compares them only when they
    start from the same operational situation.
    """

    current_prefix = tuple(epistemic_prefix)
    if current_prefix != ontic_model.actuality:
        raise ValueError(
            "epistemic and ontic models must start from the same current Actuality"
        )

    epistemic_before_view = project_epistemic_view(
        epistemic_model,
        current_prefix,
    )
    ontic_before_view = project_ontic_view(ontic_model)
    epistemic_before = operationalize_epistemic_view(epistemic_before_view)
    ontic_before = operationalize_ontic_view(ontic_before_view)
    before_comparison = compare_operational_views(
        epistemic_before,
        ontic_before,
    )

    selected_before = selected_history(epistemic_model)
    updated_epistemic_model, updated_epistemic_prefix = condition_epistemic_model(
        epistemic_model,
        current_prefix,
        observed_next,
    )
    updated_ontic_model = update_ontic_model(
        ontic_model,
        observed_next,
    )

    if updated_epistemic_prefix != updated_ontic_model.actuality:
        raise AssertionError(
            "common observation produced different updated Actualities"
        )

    epistemic_after_view = project_epistemic_view(
        updated_epistemic_model,
        updated_epistemic_prefix,
    )
    ontic_after_view = project_ontic_view(updated_ontic_model)
    epistemic_after = operationalize_epistemic_view(epistemic_after_view)
    ontic_after = operationalize_ontic_view(ontic_after_view)
    after_comparison = compare_operational_views(
        epistemic_after,
        ontic_after,
    )

    selected_after = selected_history(updated_epistemic_model)
    return Stage2UpdateComparison(
        observed_next=observed_next,
        epistemic_before=epistemic_before,
        ontic_before=ontic_before,
        before_comparison=before_comparison,
        epistemic_after=epistemic_after,
        ontic_after=ontic_after,
        after_comparison=after_comparison,
        epistemic_selected_history_before=selected_before,
        epistemic_selected_history_after=selected_after,
        epistemic_selected_history_preserved=selected_before == selected_after,
        updated_epistemic_model=updated_epistemic_model,
        updated_epistemic_prefix=updated_epistemic_prefix,
        updated_ontic_model=updated_ontic_model,
    )

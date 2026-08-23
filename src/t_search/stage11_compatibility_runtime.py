"""Runtime cache for the exhaustive Stage 11E square audit.

The Stage 11E scientific object is defined in ``stage11_compatibility``.  The
exhaustive audit crosses the same finite Stage 10 chart forms with twelve
external-parameterization edges, so evaluating the identical Born quadratic
form thousands of times adds no evidence.  This adapter memoizes probability
evaluations by the complete typed numerical chart payload (continuation,
clock/readout, normalization matrix, effect matrices, and tolerance).

The cache changes only evaluation cost.  It does not identify distinct chart
forms, weaken any square count, or alter the wrong-path control: a mislabeled
chart has different matrix bytes and therefore receives a distinct cache key.
"""

from __future__ import annotations

from functools import lru_cache
from typing import Any

import numpy as np

from .stage5_clock_change import DEFAULT_ATOL
from .stage10_probability import stage10d_chart_probabilities as _raw_probabilities
from . import stage11_compatibility as _core

_PROBABILITY_CACHE: dict[tuple[object, ...], tuple[tuple[str, float], ...]] = {}


def _array_key(value: np.ndarray) -> tuple[tuple[int, ...], str, bytes]:
    array = np.ascontiguousarray(np.asarray(value))
    return array.shape, array.dtype.str, array.tobytes()


def _cached_probabilities(
    continuation: Any,
    chart: Any,
    *,
    physical_coordinates: np.ndarray | None = None,
    normalization: np.ndarray | None = None,
    atol: float = DEFAULT_ATOL,
) -> tuple[tuple[str, float], ...]:
    # Stage 11E itself uses the canonical state and chart normalization.  Keep
    # the more general Stage 10D probe/normalization API semantically untouched.
    if physical_coordinates is not None or normalization is not None:
        return _raw_probabilities(
            continuation,
            chart,
            physical_coordinates=physical_coordinates,
            normalization=normalization,
            atol=atol,
        )

    key = (
        continuation.continuation_id,
        chart.family_id,
        chart.continuation_id,
        chart.clock,
        chart.clock_index,
        chart.prediction_anchor,
        chart.target_event,
        chart.class_correspondence,
        chart.event_correspondence,
        chart.outcome_correspondence,
        chart.normalization_semantics,
        _array_key(chart.normalization_form),
        tuple(
            (
                effect.outcome_id,
                effect.outcome_semantics,
                effect.outcome_provenance,
                _array_key(effect.matrix),
            )
            for effect in chart.effects
        ),
        float(atol),
    )
    cached = _PROBABILITY_CACHE.get(key)
    if cached is None:
        cached = _raw_probabilities(continuation, chart, atol=atol)
        _PROBABILITY_CACHE[key] = cached
    return cached


def _with_cache(function, *args, **kwargs):
    original = _core.stage10d_chart_probabilities
    _core.stage10d_chart_probabilities = _cached_probabilities
    try:
        return function(*args, **kwargs)
    finally:
        _core.stage10d_chart_probabilities = original


@lru_cache(maxsize=None)
def stage11e_diagnostics(*, atol: float = DEFAULT_ATOL):
    return _with_cache(_core.stage11e_diagnostics, atol=atol)


def stage11e_wrong_path_control(*, atol: float = DEFAULT_ATOL):
    return _with_cache(_core.stage11e_wrong_path_control, atol=atol)


def stage11e_summary(*, atol: float = DEFAULT_ATOL) -> dict[str, object]:
    return _with_cache(_core.stage11e_summary, atol=atol)


def stage11e_probability_cache_size() -> int:
    return len(_PROBABILITY_CACHE)
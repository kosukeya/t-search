"""Stage 11A minimal parametrized constrained carrier.

This module implements the classical parametrized-mechanics scaffold frozen in
Stage 11.0. The external parameter is a representation label, not physical
time. A single sampled constraint orbit is represented in four admissible
orientation-preserving parameterizations. Physical events are matched by
explicit event identity while their raw parameter values are allowed to differ.
"""

from __future__ import annotations

from dataclasses import dataclass

import numpy as np

STAGE11A_ATOL = 1.0e-10

STAGE11A_IDENTITY = "identity"
STAGE11A_AFFINE = "affine"
STAGE11A_CUBIC = "cubic"
STAGE11A_HYPERBOLIC = "hyperbolic"
STAGE11A_REVERSE = "orientation_reverse"
STAGE11A_NONINJECTIVE = "noninjective_square"

STAGE11A_POSITIVE_PARAMETERIZATION_IDS = (
    STAGE11A_IDENTITY,
    STAGE11A_AFFINE,
    STAGE11A_CUBIC,
    STAGE11A_HYPERBOLIC,
)


@dataclass(frozen=True, slots=True)
class Stage11Parameterization:
    parameterization_id: str
    description: str
    admissible: bool
    orientation_preserving: bool
    injective_on_test_domain: bool
    boundary_role: str


@dataclass(frozen=True, slots=True)
class Stage11ParametrizedTrajectory:
    parameterization_id: str
    event_ids: tuple[str, ...]
    source_labels: np.ndarray
    parameter_labels: np.ndarray
    clock_values: np.ndarray
    q_values: np.ndarray
    p_values: np.ndarray
    p_T_values: np.ndarray
    lapse_values: np.ndarray
    raw_q_rates: np.ndarray
    constraint_values: np.ndarray


@dataclass(frozen=True, slots=True)
class Stage11EventCorrespondence:
    event_id: str
    source_parameterization_id: str
    target_parameterization_id: str
    source_parameter_value: float
    target_parameter_value: float
    clock_value: float
    q_value: float


@dataclass(frozen=True, slots=True)
class Stage11ADiagnostics:
    event_count: int
    positive_parameterization_count: int
    minimum_positive_lapse: float
    max_constraint_residual: float
    max_lapse_chain_rule_residual: float
    max_clock_orbit_residual: float
    max_q_orbit_residual: float
    max_p_orbit_residual: float
    max_p_T_orbit_residual: float
    differing_parameter_event_pairs: int
    nonlinear_raw_rate_difference_count: int
    positive_family_admissible: bool
    constraint_orbit_preserved: bool
    orientation_reverse_excluded: bool
    noninjective_excluded: bool
    criteria_11_16_satisfied: bool


def canonical_stage11a_parameterizations() -> tuple[Stage11Parameterization, ...]:
    return (
        Stage11Parameterization(
            STAGE11A_IDENTITY,
            "f_id(lambda)=lambda",
            True,
            True,
            True,
            "positive admissible reference representation",
        ),
        Stage11Parameterization(
            STAGE11A_AFFINE,
            "f_aff(lambda)=2 lambda + 1",
            True,
            True,
            True,
            "positive admissible affine representation",
        ),
        Stage11Parameterization(
            STAGE11A_CUBIC,
            "f_cub(lambda)=lambda + lambda^3/4",
            True,
            True,
            True,
            "positive admissible nonlinear cubic representation",
        ),
        Stage11Parameterization(
            STAGE11A_HYPERBOLIC,
            "f_sinh(lambda)=sinh(lambda)",
            True,
            True,
            True,
            "positive admissible nonlinear hyperbolic representation",
        ),
    )


def stage11a_excluded_parameterizations() -> tuple[Stage11Parameterization, ...]:
    return (
        Stage11Parameterization(
            STAGE11A_REVERSE,
            "f_rev(lambda)=-lambda",
            False,
            False,
            True,
            "orientation-reversal boundary control; outside initial positive gauge family",
        ),
        Stage11Parameterization(
            STAGE11A_NONINJECTIVE,
            "f_noninj(lambda)=lambda^2",
            False,
            False,
            False,
            "non-injective relabeling control on a domain containing both signs",
        ),
    )


def _parameter_map(parameterization_id: str, source_labels: np.ndarray) -> np.ndarray:
    x = np.asarray(source_labels, dtype=float)
    if parameterization_id == STAGE11A_IDENTITY:
        return x.copy()
    if parameterization_id == STAGE11A_AFFINE:
        return 2.0 * x + 1.0
    if parameterization_id == STAGE11A_CUBIC:
        return x + x**3 / 4.0
    if parameterization_id == STAGE11A_HYPERBOLIC:
        return np.sinh(x)
    if parameterization_id == STAGE11A_REVERSE:
        return -x
    if parameterization_id == STAGE11A_NONINJECTIVE:
        return x**2
    raise ValueError(f"unknown Stage 11A parameterization {parameterization_id!r}")


def _parameter_jacobian(parameterization_id: str, source_labels: np.ndarray) -> np.ndarray:
    x = np.asarray(source_labels, dtype=float)
    if parameterization_id == STAGE11A_IDENTITY:
        return np.ones_like(x)
    if parameterization_id == STAGE11A_AFFINE:
        return np.full_like(x, 2.0)
    if parameterization_id == STAGE11A_CUBIC:
        return 1.0 + 3.0 * x**2 / 4.0
    if parameterization_id == STAGE11A_HYPERBOLIC:
        return np.cosh(x)
    if parameterization_id == STAGE11A_REVERSE:
        return -np.ones_like(x)
    if parameterization_id == STAGE11A_NONINJECTIVE:
        return 2.0 * x
    raise ValueError(f"unknown Stage 11A parameterization {parameterization_id!r}")


def canonical_stage11a_source_labels() -> np.ndarray:
    # Contains both signs so the square-map boundary control is visibly non-injective.
    return np.linspace(-1.5, 1.5, 13, dtype=float)


def canonical_stage11a_event_ids(count: int = 13) -> tuple[str, ...]:
    if count <= 0:
        raise ValueError("Stage 11A event count must be positive")
    return tuple(f"orbit_event_{index:02d}" for index in range(count))


def stage11a_seed_lapse(source_labels: np.ndarray) -> np.ndarray:
    x = np.asarray(source_labels, dtype=float)
    # Positive everywhere; chosen to be nonconstant so the carrier is not a
    # disguised uniform-step trajectory.
    return 1.0 + x**2 / 4.0


def stage11a_seed_clock(source_labels: np.ndarray) -> np.ndarray:
    x = np.asarray(source_labels, dtype=float)
    # Integral of N=1+x^2/4 with T(0)=0.
    return x + x**3 / 12.0


def canonical_stage11a_trajectory(
    parameterization_id: str,
    *,
    source_labels: np.ndarray | None = None,
    q0: float = -0.35,
    momentum: float = 1.25,
) -> Stage11ParametrizedTrajectory:
    specs = {
        item.parameterization_id: item
        for item in (*canonical_stage11a_parameterizations(), *stage11a_excluded_parameterizations())
    }
    if parameterization_id not in specs:
        raise ValueError(f"unknown Stage 11A parameterization {parameterization_id!r}")
    spec = specs[parameterization_id]
    if not spec.admissible:
        raise ValueError(
            f"{parameterization_id!r} is a Stage 11A boundary/control, not an admissible positive parameterization"
        )

    x = (
        canonical_stage11a_source_labels()
        if source_labels is None
        else np.asarray(source_labels, dtype=float)
    )
    if x.ndim != 1 or x.size < 3:
        raise ValueError(
            "Stage 11A source labels must be a one-dimensional sample of at least three events"
        )
    if not np.all(np.diff(x) > 0.0):
        raise ValueError("Stage 11A source labels must be strictly increasing")

    labels = _parameter_map(parameterization_id, x)
    jacobian = _parameter_jacobian(parameterization_id, x)
    if not np.all(jacobian > 0.0) or not np.all(np.diff(labels) > 0.0):
        raise ValueError(
            "admissible Stage 11A parameterization must be orientation-preserving and injective"
        )

    seed_lapse = stage11a_seed_lapse(x)
    lapse = seed_lapse / jacobian
    clock = stage11a_seed_clock(x)
    p = np.full_like(x, float(momentum))
    p_T = np.full_like(x, -0.5 * float(momentum) ** 2)
    q = float(q0) + float(momentum) * clock
    raw_q_rate = lapse * p
    constraint = p_T + 0.5 * p**2

    return Stage11ParametrizedTrajectory(
        parameterization_id=parameterization_id,
        event_ids=canonical_stage11a_event_ids(x.size),
        source_labels=x.copy(),
        parameter_labels=labels,
        clock_values=clock,
        q_values=q,
        p_values=p,
        p_T_values=p_T,
        lapse_values=lapse,
        raw_q_rates=raw_q_rate,
        constraint_values=constraint,
    )


def canonical_stage11a_positive_family() -> tuple[Stage11ParametrizedTrajectory, ...]:
    return tuple(
        canonical_stage11a_trajectory(item.parameterization_id)
        for item in canonical_stage11a_parameterizations()
    )


def stage11a_event_correspondence(
    source: Stage11ParametrizedTrajectory,
    target: Stage11ParametrizedTrajectory,
) -> tuple[Stage11EventCorrespondence, ...]:
    if source.event_ids != target.event_ids:
        raise ValueError("Stage 11A event correspondence requires the same explicit event-id carrier")
    if source.clock_values.shape != target.clock_values.shape:
        raise ValueError("Stage 11A event correspondence requires equal event counts")

    result = []
    for index, event_id in enumerate(source.event_ids):
        if not np.isclose(
            source.clock_values[index],
            target.clock_values[index],
            atol=STAGE11A_ATOL,
            rtol=0.0,
        ):
            raise ValueError(
                "Stage 11A correspondence cannot identify different physical clock values"
            )
        if not np.isclose(
            source.q_values[index], target.q_values[index], atol=STAGE11A_ATOL, rtol=0.0
        ):
            raise ValueError("Stage 11A correspondence cannot identify different q values")
        result.append(
            Stage11EventCorrespondence(
                event_id=event_id,
                source_parameterization_id=source.parameterization_id,
                target_parameterization_id=target.parameterization_id,
                source_parameter_value=float(source.parameter_labels[index]),
                target_parameter_value=float(target.parameter_labels[index]),
                clock_value=float(source.clock_values[index]),
                q_value=float(source.q_values[index]),
            )
        )
    return tuple(result)


def stage11a_lapse_chain_rule_residual(
    trajectory: Stage11ParametrizedTrajectory,
) -> float:
    source_lapse = stage11a_seed_lapse(trajectory.source_labels)
    jacobian = _parameter_jacobian(
        trajectory.parameterization_id, trajectory.source_labels
    )
    predicted = source_lapse / jacobian
    return float(np.max(np.abs(trajectory.lapse_values - predicted)))


def stage11a_diagnostics() -> Stage11ADiagnostics:
    family = canonical_stage11a_positive_family()
    reference = family[0]

    min_lapse = min(float(np.min(item.lapse_values)) for item in family)
    max_constraint = max(
        float(np.max(np.abs(item.constraint_values))) for item in family
    )
    max_chain = max(stage11a_lapse_chain_rule_residual(item) for item in family)

    max_clock = 0.0
    max_q = 0.0
    max_p = 0.0
    max_p_T = 0.0
    differing_pairs = 0
    nonlinear_rate_differences = 0

    for item in family[1:]:
        stage11a_event_correspondence(reference, item)
        max_clock = max(
            max_clock,
            float(np.max(np.abs(item.clock_values - reference.clock_values))),
        )
        max_q = max(max_q, float(np.max(np.abs(item.q_values - reference.q_values))))
        max_p = max(max_p, float(np.max(np.abs(item.p_values - reference.p_values))))
        max_p_T = max(
            max_p_T,
            float(np.max(np.abs(item.p_T_values - reference.p_T_values))),
        )
        differing_pairs += int(
            np.count_nonzero(
                np.abs(item.parameter_labels - reference.parameter_labels) > STAGE11A_ATOL
            )
        )
        if item.parameterization_id in (STAGE11A_CUBIC, STAGE11A_HYPERBOLIC):
            nonlinear_rate_differences += int(
                np.count_nonzero(
                    np.abs(item.raw_q_rates - reference.raw_q_rates) > STAGE11A_ATOL
                )
            )

    positive_specs = canonical_stage11a_parameterizations()
    excluded = {
        item.parameterization_id: item for item in stage11a_excluded_parameterizations()
    }
    positive_family_admissible = all(
        item.admissible and item.orientation_preserving and item.injective_on_test_domain
        for item in positive_specs
    )
    orbit_preserved = (
        max_clock <= STAGE11A_ATOL
        and max_q <= STAGE11A_ATOL
        and max_p <= STAGE11A_ATOL
        and max_p_T <= STAGE11A_ATOL
    )
    reverse_excluded = (
        not excluded[STAGE11A_REVERSE].admissible
        and not excluded[STAGE11A_REVERSE].orientation_preserving
    )
    noninjective_excluded = (
        not excluded[STAGE11A_NONINJECTIVE].admissible
        and not excluded[STAGE11A_NONINJECTIVE].injective_on_test_domain
    )
    criteria = (
        min_lapse > 0.0
        and max_constraint <= STAGE11A_ATOL
        and positive_family_admissible
        and differing_pairs > 0
        and max_chain <= STAGE11A_ATOL
        and orbit_preserved
        and reverse_excluded
        and noninjective_excluded
    )

    return Stage11ADiagnostics(
        event_count=len(reference.event_ids),
        positive_parameterization_count=len(family),
        minimum_positive_lapse=min_lapse,
        max_constraint_residual=max_constraint,
        max_lapse_chain_rule_residual=max_chain,
        max_clock_orbit_residual=max_clock,
        max_q_orbit_residual=max_q,
        max_p_orbit_residual=max_p,
        max_p_T_orbit_residual=max_p_T,
        differing_parameter_event_pairs=differing_pairs,
        nonlinear_raw_rate_difference_count=nonlinear_rate_differences,
        positive_family_admissible=positive_family_admissible,
        constraint_orbit_preserved=orbit_preserved,
        orientation_reverse_excluded=reverse_excluded,
        noninjective_excluded=noninjective_excluded,
        criteria_11_16_satisfied=criteria,
    )


def stage11a_summary() -> dict[str, object]:
    diagnostics = stage11a_diagnostics()
    return {
        "status": (
            "Stage 11A completed; criteria 11–16 satisfied"
            if diagnostics.criteria_11_16_satisfied
            else "Stage 11A incomplete"
        ),
        "constraint": "C = p_T + p^2/2 = 0",
        "positive_parameterizations": STAGE11A_POSITIVE_PARAMETERIZATION_IDS,
        "event_count": diagnostics.event_count,
        "minimum_positive_lapse": diagnostics.minimum_positive_lapse,
        "max_constraint_residual": diagnostics.max_constraint_residual,
        "max_lapse_chain_rule_residual": diagnostics.max_lapse_chain_rule_residual,
        "differing_parameter_event_pairs": diagnostics.differing_parameter_event_pairs,
        "nonlinear_raw_rate_difference_count": diagnostics.nonlinear_raw_rate_difference_count,
        "constraint_orbit_preserved": diagnostics.constraint_orbit_preserved,
        "excluded_controls": (STAGE11A_REVERSE, STAGE11A_NONINJECTIVE),
        "guard": "same constraint orbit != established general covariance",
    }

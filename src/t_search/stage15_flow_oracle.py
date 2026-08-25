"""Independent Hamiltonian-flow oracle for Stage 15B.

This module exists to prevent the positive-surface chart used by
``stage15_paths`` from making payload preservation tautological.  It integrates
Q and the clock coordinates directly from the Hamiltonian vector fields of the
frozen C_i and constant-smeared C[N] generators.  It does not reconstruct Q
from Q_D and it preserves the source momenta explicitly.

The oracle is a Stage 15B validation device, not an additional physical model.
"""

from __future__ import annotations

from .stage15_local import (
    STAGE15A_ATOL,
    STAGE15A_C,
    STAGE15A_KAPPA,
    Stage15PhaseSpacePoint,
    stage15a_constraints,
)


def _require_on_surface(point: Stage15PhaseSpacePoint) -> None:
    if max(abs(value) for value in stage15a_constraints(point)) > STAGE15A_ATOL:
        raise ValueError("Stage 15B Hamiltonian oracle requires an on-surface source")


def _endpoint(
    point: Stage15PhaseSpacePoint,
    *,
    Q: float,
    T0: float,
    T1: float,
    T2: float,
) -> Stage15PhaseSpacePoint:
    return Stage15PhaseSpacePoint(
        Q=float(Q),
        P=float(point.P),
        T0=float(T0),
        pi0=float(point.pi0),
        T1=float(T1),
        pi1=float(point.pi1),
        T2=float(T2),
        pi2=float(point.pi2),
    )


def stage15b_direct_local_flow(
    point: Stage15PhaseSpacePoint,
    generator_index: int,
    parameter: float,
) -> Stage15PhaseSpacePoint:
    """Integrate one local Hamiltonian vector field directly on-surface."""

    _require_on_surface(point)
    kappa = STAGE15A_KAPPA
    c0, c1, c2 = STAGE15A_C
    s = float(parameter)

    if generator_index == 0:
        dT0 = s
        dT1 = float(kappa * (point.T0 * s + 0.5 * s**2))
        return _endpoint(
            point,
            Q=float(point.Q + c0 * dT0 + c1 * dT1),
            T0=float(point.T0 + dT0),
            T1=float(point.T1 + dT1),
            T2=point.T2,
        )
    if generator_index == 1:
        dT1 = s
        dT2 = float(kappa * (point.T1 * s + 0.5 * s**2))
        return _endpoint(
            point,
            Q=float(point.Q + c1 * dT1 + c2 * dT2),
            T0=point.T0,
            T1=float(point.T1 + dT1),
            T2=float(point.T2 + dT2),
        )
    if generator_index == 2:
        dT2 = s
        return _endpoint(
            point,
            Q=float(point.Q + c2 * dT2),
            T0=point.T0,
            T1=point.T1,
            T2=float(point.T2 + dT2),
        )
    raise ValueError(f"unknown Stage 15B local generator index: {generator_index}")


def stage15b_direct_smeared_flow(
    point: Stage15PhaseSpacePoint,
    smearing: tuple[float, float, float],
    parameter: float,
) -> Stage15PhaseSpacePoint:
    """Integrate the constant-smeared Hamiltonian vector field directly."""

    _require_on_surface(point)
    n0, n1, n2 = (float(value) for value in smearing)
    lam = float(parameter)
    kappa = STAGE15A_KAPPA
    c0, c1, c2 = STAGE15A_C

    dT0 = float(n0 * lam)
    dT1 = float(
        n1 * lam
        + kappa * n0 * (point.T0 * lam + 0.5 * n0 * lam**2)
    )
    dT2 = float(
        n2 * lam
        + kappa
        * n1
        * (
            point.T1 * lam
            + 0.5 * (n1 + kappa * n0 * point.T0) * lam**2
            + (kappa * n0**2 * lam**3) / 6.0
        )
    )
    return _endpoint(
        point,
        Q=float(point.Q + c0 * dT0 + c1 * dT1 + c2 * dT2),
        T0=float(point.T0 + dT0),
        T1=float(point.T1 + dT1),
        T2=float(point.T2 + dT2),
    )

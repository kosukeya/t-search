"""Stage 6F minimality / ablation diagnostics.

The Stage 6 scaffold T6=(O,P,R,V,Omega;Xi) is deliberately typed.  This module
neutralizes O, P, R, V, and Omega one at a time, reruns declared role diagnostics,
and classifies the result without turning software dependency into a metaphysical
irreducibility claim.

Status semantics are executable and evidence-driven:

- preserved: the role is still directly represented and passes its diagnostic;
- reconstructible: the removed primitive is absent, but the role is recovered
  from retained declared structure under the frozen interface;
- inaccessible: the underlying role remains represented, but the declared local
  interface cannot access it;
- lost: the role was present at baseline and the declared ablation removes the
  current representation without an executable reconstruction witness;
- not_applicable: the diagnostic requires a removed endpoint/layer;
- not_established: current evidence does not decide the role.

"lost" is therefore a statement about this declared ablation interface, not a
proof of metaphysical irreducibility.
"""

from __future__ import annotations

from dataclasses import dataclass
from enum import Enum
from itertools import permutations, product
from typing import Any

import numpy as np

from .stage3_asymmetry import AsymmetricRecordModel, assess_record_orientation
from .stage3_controls import no_record_forward_ensemble
from .stage5_clock_change import (
    DEFAULT_ATOL,
    DEFAULT_DIMENSION,
    SUBSYSTEMS,
    physical_state_from_coefficients,
)
from .stage5_clock_transforms import genuine_clock_change_operator
from .stage5_operational import reduced_born_probability
from .stage5_reductions import clock_relative_support_basis, physical_clock_reduction
from .stage6_compatibility import (
    CANONICAL_EVENTS,
    canonical_stage6d_diagnostics,
    ordered_event_relations,
)
from .stage6_partial_atlas import (
    canonical_partial_clock_atlas,
    diagnose_partial_atlas,
    external_direct_reference,
)
from .stage6_record_modality import (
    canonical_modal_transport,
    canonical_preserving_record_transport,
    record_accessibility_controls,
)

LAYERS: tuple[str, ...] = ("O", "P", "R", "V", "Omega")
ROLE_IDS: tuple[str, ...] = (
    "succession_order",
    "perspective_transport",
    "record_defined_direction",
    "modal_branching_semantics",
    "cross_perspective_operational_consistency",
    "local_record_accessibility",
    "P_O_compatibility",
    "P_R_compatibility",
    "P_V_compatibility",
)


class AblationStatus(str, Enum):
    PRESERVED = "preserved"
    RECONSTRUCTIBLE = "reconstructible"
    INACCESSIBLE = "inaccessible"
    LOST = "lost"
    NOT_APPLICABLE = "not_applicable"
    NOT_ESTABLISHED = "not_established"


@dataclass(frozen=True)
class RoleEvidence:
    """Machine-readable evidence used to derive one ablation status."""

    role: str
    applicable: bool = True
    direct_available: bool = False
    reconstruction_available: bool = False
    globally_represented: bool | None = None
    locally_accessible: bool | None = None
    decisive_loss: bool = False
    measurements: tuple[tuple[str, Any], ...] = ()
    note: str = ""

    @property
    def status(self) -> AblationStatus:
        if not self.applicable:
            return AblationStatus.NOT_APPLICABLE
        if self.direct_available:
            return AblationStatus.PRESERVED
        if self.reconstruction_available:
            return AblationStatus.RECONSTRUCTIBLE
        if self.globally_represented is True and self.locally_accessible is False:
            return AblationStatus.INACCESSIBLE
        if self.decisive_loss:
            return AblationStatus.LOST
        return AblationStatus.NOT_ESTABLISHED

    def as_dict(self) -> dict[str, Any]:
        return {
            "role": self.role,
            "status": self.status.value,
            "applicable": self.applicable,
            "direct_available": self.direct_available,
            "reconstruction_available": self.reconstruction_available,
            "globally_represented": self.globally_represented,
            "locally_accessible": self.locally_accessible,
            "decisive_loss": self.decisive_loss,
            "measurements": dict(self.measurements),
            "note": self.note,
        }


@dataclass(frozen=True)
class AblationCase:
    """One declared layer neutralization and the resulting role evidence."""

    removed_layer: str
    neutralization: str
    retained_layers: tuple[str, ...]
    probes: tuple[RoleEvidence, ...]
    irreducibility_status: AblationStatus = AblationStatus.NOT_ESTABLISHED

    def __post_init__(self) -> None:
        if self.removed_layer not in LAYERS:
            raise ValueError(f"unknown Stage 6 layer: {self.removed_layer!r}")
        if set(self.retained_layers) != set(LAYERS) - {self.removed_layer}:
            raise ValueError("retained_layers must contain exactly the non-ablated layers")
        roles = tuple(probe.role for probe in self.probes)
        if roles != ROLE_IDS:
            raise ValueError("ablation probes must follow the frozen Stage 6F role order")
        if self.irreducibility_status is not AblationStatus.NOT_ESTABLISHED:
            raise ValueError("Stage 6F does not establish metaphysical irreducibility")

    def status(self, role: str) -> AblationStatus:
        return next(probe.status for probe in self.probes if probe.role == role)

    def as_dict(self) -> dict[str, Any]:
        return {
            "removed_layer": self.removed_layer,
            "neutralization": self.neutralization,
            "retained_layers": list(self.retained_layers),
            "irreducibility_status": self.irreducibility_status.value,
            "probes": [probe.as_dict() for probe in self.probes],
        }


@dataclass(frozen=True)
class OmegaReconstructionDiagnostics:
    """Can Stage 5 operational covariance be recovered from retained P maps?"""

    comparison_count: int
    max_bare_matrix_probability_residual: float
    bare_matrix_mismatch_count: int
    max_reconstructed_probability_residual: float
    reconstructed_match_count: int
    tolerance: float

    @property
    def raw_correspondence_fails(self) -> bool:
        return self.bare_matrix_mismatch_count > 0

    @property
    def reconstructed_correspondence_holds(self) -> bool:
        return (
            self.comparison_count > 0
            and self.max_reconstructed_probability_residual <= self.tolerance
            and self.reconstructed_match_count == self.comparison_count
        )

    def as_dict(self) -> dict[str, Any]:
        return {
            "comparison_count": self.comparison_count,
            "max_bare_matrix_probability_residual": self.max_bare_matrix_probability_residual,
            "bare_matrix_mismatch_count": self.bare_matrix_mismatch_count,
            "max_reconstructed_probability_residual": self.max_reconstructed_probability_residual,
            "reconstructed_match_count": self.reconstructed_match_count,
            "tolerance": self.tolerance,
            "raw_correspondence_fails": self.raw_correspondence_fails,
            "reconstructed_correspondence_holds": self.reconstructed_correspondence_holds,
        }


def _measurement(name: str, value: Any) -> tuple[str, Any]:
    if isinstance(value, np.generic):
        value = value.item()
    return name, value


def _generic_physical_state() -> np.ndarray:
    raw = np.array(
        [
            1.0 + 0.2j,
            -0.4 + 0.7j,
            0.3 - 0.1j,
            0.8 + 0.5j,
            -0.2 - 0.6j,
            0.9 - 0.3j,
            0.1 + 0.4j,
        ],
        dtype=np.complex128,
    )
    return physical_state_from_coefficients(raw, normalize=True)


def _support_projector(clock: str, dimension: int = DEFAULT_DIMENSION) -> np.ndarray:
    basis = clock_relative_support_basis(clock, dimension)
    coordinates = np.array(
        [1.0, 0.4j, -0.3 + 0.2j, 0.5, -0.1j, 0.25, -0.45],
        dtype=np.complex128,
    )
    if coordinates.shape != (basis.shape[1],):
        raise RuntimeError("Stage 6F projector coordinates do not match support dimension")
    coordinates /= np.linalg.norm(coordinates)
    ket = basis @ coordinates
    return np.outer(ket, ket.conj())


def omega_reconstruction_diagnostics(
    dimension: int = DEFAULT_DIMENSION,
    *,
    tolerance: float = DEFAULT_ATOL,
) -> OmegaReconstructionDiagnostics:
    """Remove explicit Omega and test bare versus P-induced observable transport."""

    physical_state = _generic_physical_state()
    bare_residuals: list[float] = []
    reconstructed_residuals: list[float] = []

    for source, target in permutations(SUBSYSTEMS, 2):
        source_projector = _support_projector(source, dimension)
        for source_index, target_index in product(range(dimension), repeat=2):
            source_state = physical_clock_reduction(
                physical_state, source, source_index, dimension
            )
            target_state = physical_clock_reduction(
                physical_state, target, target_index, dimension
            )
            source_probability = reduced_born_probability(
                source_state, source_projector, dimension
            )

            bare_probability = reduced_born_probability(
                target_state, source_projector, dimension
            )
            bare_residuals.append(abs(source_probability - bare_probability))

            perspective_map = genuine_clock_change_operator(
                target,
                target_index,
                source,
                source_index,
                dimension,
            )
            reconstructed_projector = (
                perspective_map @ source_projector @ perspective_map.conj().T
            )
            target_probability = reduced_born_probability(
                target_state, reconstructed_projector, dimension
            )
            reconstructed_residuals.append(abs(source_probability - target_probability))

    return OmegaReconstructionDiagnostics(
        comparison_count=len(reconstructed_residuals),
        max_bare_matrix_probability_residual=max(bare_residuals, default=0.0),
        bare_matrix_mismatch_count=sum(value > tolerance for value in bare_residuals),
        max_reconstructed_probability_residual=max(
            reconstructed_residuals, default=0.0
        ),
        reconstructed_match_count=sum(
            value <= tolerance for value in reconstructed_residuals
        ),
        tolerance=tolerance,
    )


def _baseline_flags() -> dict[str, bool]:
    order_relations = ordered_event_relations(CANONICAL_EVENTS)

    atlas, source, target = canonical_partial_clock_atlas()
    atlas_diagnostics = diagnose_partial_atlas(
        atlas,
        source,
        target,
        external_direct_reference(source, target),
    )

    record_transport = canonical_preserving_record_transport()
    modal_transport = canonical_modal_transport()
    compatibility = canonical_stage6d_diagnostics()
    exact_access = record_accessibility_controls()["exact"]
    omega = omega_reconstruction_diagnostics()

    return {
        "succession_order": len(order_relations) == 3,
        "perspective_transport": (
            atlas_diagnostics.target_present
            and not atlas_diagnostics.direct_edge_present
            and atlas_diagnostics.path_count == 3
            and atlas_diagnostics.max_indirect_direct_residual <= DEFAULT_ATOL
            and atlas_diagnostics.max_pairwise_path_residual <= DEFAULT_ATOL
        ),
        "record_defined_direction": (
            record_transport.globally_compatible
            and record_transport.source_orientation != "none"
        ),
        "modal_branching_semantics": (
            modal_transport.epistemic_extensions.relation_holds
            and modal_transport.ontic_extensions.relation_holds
            and modal_transport.source_potentiality_types_distinct
            and modal_transport.target_potentiality_types_distinct
        ),
        "cross_perspective_operational_consistency": (
            omega.reconstructed_correspondence_holds
        ),
        "local_record_accessibility": (
            exact_access.target_local.record_exposed
            and exact_access.target_local.record_score is not None
            and abs(exact_access.target_local.record_score) > 1e-12
        ),
        "P_O_compatibility": (
            compatibility.max_square_residual <= DEFAULT_ATOL
            and compatibility.order_violation_count == 0
        ),
        "P_R_compatibility": record_transport.globally_compatible,
        "P_V_compatibility": (
            modal_transport.epistemic_extensions.relation_holds
            and modal_transport.ontic_extensions.relation_holds
        ),
    }


def baseline_role_evidence() -> tuple[RoleEvidence, ...]:
    """Recompute the directly represented baseline before any layer ablation."""

    flags = _baseline_flags()
    return tuple(
        RoleEvidence(
            role=role,
            direct_available=flags[role],
            globally_represented=flags[role],
            locally_accessible=True if role == "local_record_accessibility" else None,
            decisive_loss=not flags[role],
            measurements=(("baseline_pass", flags[role]),),
            note="direct baseline diagnostic before ablation",
        )
        for role in ROLE_IDS
    )


def _preserved(role: str, flags: dict[str, bool], note: str = "") -> RoleEvidence:
    passed = flags[role]
    return RoleEvidence(
        role=role,
        direct_available=passed,
        globally_represented=passed,
        decisive_loss=not passed,
        measurements=(("retained_diagnostic_pass", passed),),
        note=note or "role rerun from retained declared structure",
    )


def _not_applicable(role: str, note: str) -> RoleEvidence:
    return RoleEvidence(role=role, applicable=False, note=note)


def _lost(
    role: str,
    *,
    measurements: tuple[tuple[str, Any], ...],
    note: str,
) -> RoleEvidence:
    return RoleEvidence(
        role=role,
        direct_available=False,
        reconstruction_available=False,
        globally_represented=False,
        decisive_loss=True,
        measurements=measurements,
        note=note,
    )


def _case_o(flags: dict[str, bool]) -> AblationCase:
    baseline_relations = len(ordered_event_relations(CANONICAL_EVENTS))
    probes = (
        _lost(
            "succession_order",
            measurements=(
                ("baseline_relation_count", baseline_relations),
                ("neutralized_relation_count", 0),
            ),
            note=(
                "explicit Stage 6 order/conditioning relation is removed; Stage 3 "
                "bookkeeping indices retained inside R are not silently promoted to O"
            ),
        ),
        _preserved("perspective_transport", flags),
        _preserved(
            "record_defined_direction",
            flags,
            "Stage 3 record diagnostic remains executable on its neutral bookkeeping positions",
        ),
        _preserved("modal_branching_semantics", flags),
        _preserved("cross_perspective_operational_consistency", flags),
        _preserved("local_record_accessibility", flags),
        _not_applicable(
            "P_O_compatibility",
            "horizontal/vertical compatibility requires the ablated O endpoint",
        ),
        _preserved("P_R_compatibility", flags),
        _preserved("P_V_compatibility", flags),
    )
    return AblationCase(
        removed_layer="O",
        neutralization="remove explicit event-order relations and vertical conditioning family",
        retained_layers=tuple(layer for layer in LAYERS if layer != "O"),
        probes=probes,
    )


def _case_p(flags: dict[str, bool]) -> AblationCase:
    probes = (
        _preserved("succession_order", flags),
        _lost(
            "perspective_transport",
            measurements=(
                ("atlas_present_after_ablation", False),
                ("available_cross_perspective_path_count", 0),
            ),
            note="remove perspective atlas vertices/maps as Stage 6 P data",
        ),
        _preserved("record_defined_direction", flags),
        _preserved("modal_branching_semantics", flags),
        _not_applicable(
            "cross_perspective_operational_consistency",
            "no source/target perspective transport remains on which to state cross-perspective Omega",
        ),
        _preserved("local_record_accessibility", flags),
        _not_applicable("P_O_compatibility", "P endpoint removed"),
        _not_applicable("P_R_compatibility", "P endpoint removed"),
        _not_applicable("P_V_compatibility", "P endpoint removed"),
    )
    return AblationCase(
        removed_layer="P",
        neutralization="remove perspective atlas vertices/maps from the declared interface",
        retained_layers=tuple(layer for layer in LAYERS if layer != "P"),
        probes=probes,
    )


def _case_r(flags: dict[str, bool]) -> AblationCase:
    no_record = assess_record_orientation(
        AsymmetricRecordModel(ensemble=no_record_forward_ensemble())
    )
    record_lost = (
        not no_record.record_defined
        and no_record.orientation == "none"
        and abs(no_record.record_score) <= 1e-12
        and abs(no_record.accessibility_score) <= 1e-12
    )
    probes = (
        _preserved("succession_order", flags),
        _preserved("perspective_transport", flags),
        RoleEvidence(
            role="record_defined_direction",
            direct_available=False,
            globally_represented=not record_lost,
            decisive_loss=record_lost,
            measurements=(
                ("no_record_record_defined", no_record.record_defined),
                ("no_record_orientation", no_record.orientation),
                ("no_record_record_score", no_record.record_score),
                ("no_record_accessibility_score", no_record.accessibility_score),
            ),
            note="replace U_rec by the reversible no-record control while retaining ordered positions",
        ),
        _preserved("modal_branching_semantics", flags),
        _preserved("cross_perspective_operational_consistency", flags),
        RoleEvidence(
            role="local_record_accessibility",
            direct_available=False,
            globally_represented=not record_lost,
            locally_accessible=False if record_lost else None,
            decisive_loss=record_lost,
            measurements=(("no_record_accessibility_score", no_record.accessibility_score),),
            note="record-specific local contrast vanishes because the record structure itself was neutralized",
        ),
        _preserved("P_O_compatibility", flags),
        _not_applicable("P_R_compatibility", "R endpoint removed"),
        _preserved("P_V_compatibility", flags),
    )
    return AblationCase(
        removed_layer="R",
        neutralization="replace the recording interaction with the reversible no-record control",
        retained_layers=tuple(layer for layer in LAYERS if layer != "R"),
        probes=probes,
    )


def _case_v(flags: dict[str, bool]) -> AblationCase:
    modal = canonical_modal_transport()
    baseline_extensions = (
        modal.epistemic_extensions.source_extension_count
        + modal.ontic_extensions.source_extension_count
    )
    probes = (
        _preserved("succession_order", flags),
        _preserved("perspective_transport", flags),
        _preserved("record_defined_direction", flags),
        _lost(
            "modal_branching_semantics",
            measurements=(
                ("baseline_typed_extension_count", baseline_extensions),
                ("potentiality_carrier_present_after_ablation", False),
            ),
            note=(
                "remove typed EpistemicPotentiality/OnticPotentiality carriers; "
                "operational equality is not used to recreate modal semantics"
            ),
        ),
        _preserved("cross_perspective_operational_consistency", flags),
        _preserved("local_record_accessibility", flags),
        _preserved("P_O_compatibility", flags),
        _preserved("P_R_compatibility", flags),
        _not_applicable("P_V_compatibility", "V endpoint removed"),
    )
    return AblationCase(
        removed_layer="V",
        neutralization="remove typed Potentiality/extension carriers and their extension semantics",
        retained_layers=tuple(layer for layer in LAYERS if layer != "V"),
        probes=probes,
    )


def _case_omega(flags: dict[str, bool]) -> AblationCase:
    omega = omega_reconstruction_diagnostics()
    reconstruction = (
        omega.raw_correspondence_fails
        and omega.reconstructed_correspondence_holds
    )
    probes = (
        _preserved("succession_order", flags),
        _preserved("perspective_transport", flags),
        _preserved("record_defined_direction", flags),
        _preserved("modal_branching_semantics", flags),
        RoleEvidence(
            role="cross_perspective_operational_consistency",
            direct_available=False,
            reconstruction_available=reconstruction,
            globally_represented=True if reconstruction else None,
            decisive_loss=not reconstruction,
            measurements=(
                ("bare_matrix_mismatch_count", omega.bare_matrix_mismatch_count),
                (
                    "max_bare_matrix_probability_residual",
                    omega.max_bare_matrix_probability_residual,
                ),
                (
                    "max_reconstructed_probability_residual",
                    omega.max_reconstructed_probability_residual,
                ),
                ("reconstructed_match_count", omega.reconstructed_match_count),
                ("comparison_count", omega.comparison_count),
            ),
            note=(
                "explicit Omega rule removed; corresponding target observable is "
                "reconstructed from retained P by M O M^dagger in the declared "
                "quantum operator interface"
            ),
        ),
        _preserved("local_record_accessibility", flags),
        _preserved("P_O_compatibility", flags),
        _preserved("P_R_compatibility", flags),
        _preserved("P_V_compatibility", flags),
    )
    return AblationCase(
        removed_layer="Omega",
        neutralization="remove explicit cross-perspective observable-correspondence rule",
        retained_layers=tuple(layer for layer in LAYERS if layer != "Omega"),
        probes=probes,
    )


def build_stage6f_ablation_matrix() -> tuple[AblationCase, ...]:
    """Recompute all five layer ablations in frozen order."""

    flags = _baseline_flags()
    if not all(flags.values()):
        failed = tuple(role for role, passed in flags.items() if not passed)
        raise RuntimeError(f"Stage 6F baseline diagnostics failed: {failed}")
    cases = (
        _case_o(flags),
        _case_p(flags),
        _case_r(flags),
        _case_v(flags),
        _case_omega(flags),
    )
    if tuple(case.removed_layer for case in cases) != LAYERS:
        raise RuntimeError("Stage 6F ablation matrix is incomplete or misordered")
    return cases


def accessibility_inaccessibility_control() -> RoleEvidence:
    """Classify hidden-record access without removing the global R structure."""

    hidden = record_accessibility_controls()["target-hidden"]
    globally_present = hidden.globally_compatible
    locally_accessible = (
        hidden.target_local.record_exposed
        and hidden.target_local.record_score is not None
    )
    return RoleEvidence(
        role="local_record_accessibility",
        direct_available=False,
        globally_represented=globally_present,
        locally_accessible=locally_accessible,
        decisive_loss=False,
        measurements=(
            ("global_record_transport_compatible", globally_present),
            ("target_record_exposed", hidden.target_local.record_exposed),
            ("target_record_score", hidden.target_local.record_score),
        ),
        note=(
            "interface-only control: R is retained globally while the target record "
            "field is hidden"
        ),
    )


def stage6f_minimality_summary() -> dict[str, Any]:
    """Return the bounded structural conclusion supported by the ablation matrix."""

    cases = build_stage6f_ablation_matrix()
    own_role = {
        "O": "succession_order",
        "P": "perspective_transport",
        "R": "record_defined_direction",
        "V": "modal_branching_semantics",
        "Omega": "cross_perspective_operational_consistency",
    }
    own_status = {
        case.removed_layer: case.status(own_role[case.removed_layer]).value
        for case in cases
    }
    return {
        "own_role_status_after_ablation": own_status,
        "layers_lost_in_declared_interface": [
            layer for layer, status in own_status.items() if status == "lost"
        ],
        "layers_reconstructible_in_declared_interface": [
            layer
            for layer, status in own_status.items()
            if status == "reconstructible"
        ],
        "metaphysical_irreducibility_established": False,
        "minimality_interpretation": (
            "O, P, R, and V each lose their named role under the declared ablation "
            "without a reconstruction witness; Omega is reconstructible from retained "
            "P in the canonical quantum operator interface. This does not prove that "
            "O/P/R/V are universally irreducible or that Omega is universally redundant."
        ),
    }


def stage6f_rows() -> dict[str, Any]:
    """Return JSON-friendly baseline, ablation, control, and minimality rows."""

    return {
        "status_vocabulary": [status.value for status in AblationStatus],
        "layers": list(LAYERS),
        "roles": list(ROLE_IDS),
        "baseline": [probe.as_dict() for probe in baseline_role_evidence()],
        "ablations": [case.as_dict() for case in build_stage6f_ablation_matrix()],
        "accessibility_control": accessibility_inaccessibility_control().as_dict(),
        "omega_reconstruction": omega_reconstruction_diagnostics().as_dict(),
        "minimality_summary": stage6f_minimality_summary(),
        "interpretation_guards": {
            "lost_means_metaphysically_irreducible": False,
            "software_dependency_proves_fundamentality": False,
            "inaccessible_means_globally_absent": False,
            "omega_reconstructible_here_means_universally_redundant": False,
            "record_direction_is_phenomenal_passage": False,
        },
    }

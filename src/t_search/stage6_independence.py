"""Stage 6B independence and executable countermodel matrix.

This module consumes the Stage 6A witness inventory and derives implication
statuses from measurement-backed case facts.  It deliberately keeps unknown
conclusions distinct from false conclusions: an implication is refuted only
when an executable case has a true antecedent and a false consequent.
"""

from __future__ import annotations

from dataclasses import dataclass
from enum import Enum
from typing import Any, Iterable

from .stage6_inventory import WitnessRecord, build_stage6a_inventory


class TruthValue(str, Enum):
    """Three-valued proposition truth used by Stage 6B."""

    TRUE = "true"
    FALSE = "false"
    UNKNOWN = "unknown"


class ImplicationStatus(str, Enum):
    """Frozen Stage 6B implication-classification statuses."""

    REFUTED = "refuted"
    SUPPORTED_IN_DECLARED_FAMILY = "supported_in_declared_family"
    NOT_ESTABLISHED = "not_established"


@dataclass(frozen=True)
class PropositionFact:
    """A proposition value derived from explicit witness measurements."""

    name: str
    value: TruthValue
    measurement_names: tuple[str, ...] = ()
    note: str = ""

    def as_dict(self) -> dict[str, Any]:
        return {
            "name": self.name,
            "value": self.value.value,
            "measurement_names": list(self.measurement_names),
            "note": self.note,
        }


@dataclass(frozen=True)
class EvidenceCase:
    """One measurement-backed case used to test logical non-implications."""

    case_id: str
    witness_id: str
    source_stage: int
    domain: str
    facts: tuple[PropositionFact, ...]

    def fact(self, name: str) -> PropositionFact:
        matches = [fact for fact in self.facts if fact.name == name]
        if not matches:
            return PropositionFact(name=name, value=TruthValue.UNKNOWN)
        if len(matches) != 1:
            raise RuntimeError(f"duplicate fact {name!r} in case {self.case_id}")
        return matches[0]

    def as_dict(self) -> dict[str, Any]:
        return {
            "case_id": self.case_id,
            "witness_id": self.witness_id,
            "source_stage": self.source_stage,
            "domain": self.domain,
            "facts": {fact.name: fact.as_dict() for fact in self.facts},
        }


@dataclass(frozen=True)
class ImplicationSpec:
    """One frozen implication from the Stage 6 protocol."""

    implication_id: str
    label: str
    antecedent: str
    consequent: str
    interpretation: str


@dataclass(frozen=True)
class CaseEvidence:
    """Antecedent-true case and the measured consequent status."""

    case_id: str
    witness_id: str
    antecedent: PropositionFact
    consequent: PropositionFact

    def as_dict(self) -> dict[str, Any]:
        return {
            "case_id": self.case_id,
            "witness_id": self.witness_id,
            "antecedent": self.antecedent.as_dict(),
            "consequent": self.consequent.as_dict(),
        }


@dataclass(frozen=True)
class ImplicationAssessment:
    """Measurement-derived Stage 6B classification of one implication."""

    spec: ImplicationSpec
    status: ImplicationStatus
    evidence: tuple[CaseEvidence, ...]

    @property
    def premise_case_ids(self) -> tuple[str, ...]:
        return tuple(item.case_id for item in self.evidence)

    @property
    def countermodel_case_ids(self) -> tuple[str, ...]:
        return tuple(
            item.case_id
            for item in self.evidence
            if item.consequent.value is TruthValue.FALSE
        )

    @property
    def support_case_ids(self) -> tuple[str, ...]:
        return tuple(
            item.case_id
            for item in self.evidence
            if item.consequent.value is TruthValue.TRUE
        )

    @property
    def undecided_case_ids(self) -> tuple[str, ...]:
        return tuple(
            item.case_id
            for item in self.evidence
            if item.consequent.value is TruthValue.UNKNOWN
        )

    @property
    def witness_ids(self) -> tuple[str, ...]:
        return tuple(dict.fromkeys(item.witness_id for item in self.evidence))

    def as_dict(self) -> dict[str, Any]:
        return {
            "implication_id": self.spec.implication_id,
            "label": self.spec.label,
            "antecedent": self.spec.antecedent,
            "consequent": self.spec.consequent,
            "interpretation": self.spec.interpretation,
            "status": self.status.value,
            "witness_ids": list(self.witness_ids),
            "premise_case_ids": list(self.premise_case_ids),
            "countermodel_case_ids": list(self.countermodel_case_ids),
            "support_case_ids": list(self.support_case_ids),
            "undecided_case_ids": list(self.undecided_case_ids),
            "evidence": [item.as_dict() for item in self.evidence],
        }


FROZEN_IMPLICATIONS: tuple[ImplicationSpec, ...] = (
    ImplicationSpec(
        "I1",
        "order => arrow",
        "neutral_order_present",
        "record_arrow_present",
        (
            "For the executable Stage 3 family, 'arrow' is operationalized as "
            "the declared record-defined orientation, not phenomenal passage."
        ),
    ),
    ImplicationSpec(
        "I2",
        "reversible microdynamics => no record arrow",
        "reversible_microdynamics",
        "no_record_arrow",
        "Microscopic bijectivity is compared with the Stage 3 record diagnostic.",
    ),
    ImplicationSpec(
        "I3",
        "perspective consistency => temporal arrow",
        "perspective_consistency",
        "temporal_arrow_present",
        (
            "Perspective/transition consistency does not receive a temporal-arrow "
            "truth value unless a witness measures one explicitly."
        ),
    ),
    ImplicationSpec(
        "I4",
        "operational equality => modal/ontological equivalence",
        "operational_equality",
        "modal_ontological_equivalence",
        (
            "Formal modal/model inequivalence is witnessed by distinct declared "
            "Potentiality runtime structures under equal operational projections."
        ),
    ),
    ImplicationSpec(
        "I5",
        "global reconstructibility => local accessibility",
        "global_reconstructible",
        "local_accessibility",
        (
            "Accessibility is relative to the declared one-hop local interface, "
            "not to a theorist with the complete family of views."
        ),
    ),
    ImplicationSpec(
        "I6",
        "perspective-dependent structure => operational inconsistency",
        "perspective_dependent_structure",
        "operational_inconsistency",
        (
            "Operational consistency uses corresponding transported observables, "
            "not equality of perspective-dependent reduced structure."
        ),
    ),
    ImplicationSpec(
        "I7",
        "physical clock change => temporal succession",
        "physical_clock_change",
        "temporal_succession",
        (
            "A genuine clock-subsystem change is a horizontal perspective map; "
            "succession remains unknown unless separately measured."
        ),
    ),
    ImplicationSpec(
        "I8",
        "record arrow => ontologically open future",
        "record_arrow_present",
        "ontologically_open_future",
        (
            "Record orientation carries no automatic ontological-openness label."
        ),
    ),
    ImplicationSpec(
        "I9",
        "Potentiality => phenomenal passage",
        "potentiality_present",
        "phenomenal_passage",
        "Branching/extension structure does not itself measure phenomenal passage.",
    ),
    ImplicationSpec(
        "I10",
        "perspective consistency => modal equivalence",
        "perspective_consistency",
        "modal_ontological_equivalence",
        (
            "Perspective-map consistency and modal semantics are kept as distinct "
            "typed roles unless a witness links them."
        ),
    ),
)


def _known_bool(
    name: str,
    value: bool,
    measurement_names: tuple[str, ...],
    note: str = "",
) -> PropositionFact:
    return PropositionFact(
        name=name,
        value=TruthValue.TRUE if value else TruthValue.FALSE,
        measurement_names=measurement_names,
        note=note,
    )


def _unknown(name: str, note: str) -> PropositionFact:
    return PropositionFact(name=name, value=TruthValue.UNKNOWN, note=note)


def _tolerance(record: WitnessRecord, fallback: float = 0.0) -> float:
    return record.tolerance if record.tolerance is not None else fallback


def _w1_case(record: WitnessRecord) -> EvidenceCase:
    labeled_equal = bool(record.measurement("family_labeled_equal"))
    reachability_equal = bool(record.measurement("family_reachability_equal"))
    remote_reachable = bool(record.measurement("remote_globally_reachable"))
    remote_local = bool(record.measurement("remote_in_one_hop_view"))
    pair_count = int(record.measurement("global_reachability_pair_count"))

    facts = (
        _known_bool(
            "neutral_order_present",
            pair_count > 0,
            ("global_reachability_pair_count",),
            "A nonempty directed reachability relation supplies the declared neutral order.",
        ),
        _known_bool(
            "global_reconstructible",
            labeled_equal and reachability_equal,
            ("family_labeled_equal", "family_reachability_equal"),
        ),
        _known_bool(
            "local_accessibility",
            remote_local if remote_reachable else False,
            ("remote_globally_reachable", "remote_in_one_hop_view"),
            (
                "The selected target is globally reachable; accessibility asks "
                "whether that same target occurs in the declared one-hop view."
            ),
        )
        if remote_reachable
        else _unknown(
            "local_accessibility",
            "The selected target is not globally reachable, so this case does not decide the intended accessibility comparison.",
        ),
    )
    return EvidenceCase(
        case_id="W1:global-vs-local",
        witness_id=record.witness_id,
        source_stage=record.source_stage,
        domain=record.domain,
        facts=facts,
    )


def _w2_case(record: WitnessRecord) -> EvidenceCase:
    operational_equal = bool(record.measurement("operational_equal"))
    epistemic_live = int(record.measurement("epistemic_live_history_count"))
    ontic_live = int(record.measurement("ontic_live_history_count"))
    runtime_types_equal = bool(record.measurement("potentiality_runtime_types_equal"))

    modal_equivalence = (
        _known_bool(
            "modal_ontological_equivalence",
            False,
            ("potentiality_runtime_types_equal",),
            (
                "Distinct declared Potentiality runtime types are sufficient to "
                "refute formal modal/model equivalence in this matched comparison; "
                "runtime-type equality alone would not establish equivalence."
            ),
        )
        if not runtime_types_equal
        else _unknown(
            "modal_ontological_equivalence",
            "Runtime-type equality alone would not establish modal/ontological equivalence.",
        )
    )

    return EvidenceCase(
        case_id="W2:matched-modal-operational",
        witness_id=record.witness_id,
        source_stage=record.source_stage,
        domain=record.domain,
        facts=(
            _known_bool(
                "operational_equality",
                operational_equal,
                ("operational_equal",),
            ),
            _known_bool(
                "potentiality_present",
                epistemic_live > 1 and ontic_live > 1,
                ("epistemic_live_history_count", "ontic_live_history_count"),
                "Both matched views retain more than one live extension/history.",
            ),
            modal_equivalence,
            _unknown(
                "phenomenal_passage",
                "No Stage 2 measurement represents phenomenal passage.",
            ),
        ),
    )


def _w3_cases(record: WitnessRecord) -> tuple[EvidenceCase, ...]:
    cases: list[EvidenceCase] = []
    for control in ("forward", "reversed", "symmetric", "no-record", "uniform-memory"):
        position_name = f"{control}_declared_position_count"
        reversible_name = f"{control}_declared_microdynamics_reversible"
        record_name = f"{control}_record_defined"

        order_present = int(record.measurement(position_name)) > 1
        reversible = bool(record.measurement(reversible_name))
        record_arrow = bool(record.measurement(record_name))
        facts = (
            _known_bool(
                "neutral_order_present",
                order_present,
                (position_name,),
            ),
            _known_bool(
                "reversible_microdynamics",
                reversible,
                (reversible_name,),
            ),
            _known_bool(
                "record_arrow_present",
                record_arrow,
                (record_name, f"{control}_record_score", f"{control}_accessibility_score"),
            ),
            _known_bool(
                "no_record_arrow",
                not record_arrow,
                (record_name, f"{control}_record_score", f"{control}_accessibility_score"),
            ),
            _unknown(
                "ontologically_open_future",
                "The Stage 3 record control does not encode ontological future openness.",
            ),
        )
        cases.append(
            EvidenceCase(
                case_id=f"W3:{control}",
                witness_id=record.witness_id,
                source_stage=record.source_stage,
                domain=f"{record.domain}; control={control}",
                facts=facts,
            )
        )
    return tuple(cases)


def _w4_case(record: WitnessRecord) -> EvidenceCase:
    tol = _tolerance(record)
    residual_names = (
        "max_identity_residual",
        "max_inverse_residual",
        "max_composition_residual",
        "max_expected_transition_residual",
        "max_unitarity_residual",
    )
    consistent = all(float(record.measurement(name)) <= tol for name in residual_names)
    return EvidenceCase(
        case_id="W4:same-clock-transition-family",
        witness_id=record.witness_id,
        source_stage=record.source_stage,
        domain=record.domain,
        facts=(
            _known_bool(
                "perspective_consistency",
                consistent,
                residual_names,
                "All declared same-clock transition residuals are compared with the witness tolerance.",
            ),
            _unknown(
                "temporal_arrow_present",
                "The Stage 4 adapter intentionally does not identify reversible transition consistency with a temporal arrow.",
            ),
            _unknown(
                "modal_ontological_equivalence",
                "The Stage 4 witness carries no modal-semantics comparison.",
            ),
        ),
    )


def _w5_case(record: WitnessRecord) -> EvidenceCase:
    tol = _tolerance(record)
    route_count = int(record.measurement("three_clock_route_count"))
    composition_residual = float(
        record.measurement("max_cross_clock_composition_residual")
    )
    born_residual = float(record.measurement("max_born_probability_residual"))
    perspective_dependent = bool(
        record.measurement("entanglement_perspective_dependent")
    )

    return EvidenceCase(
        case_id="W5:cross-clock-operational",
        witness_id=record.witness_id,
        source_stage=record.source_stage,
        domain=record.domain,
        facts=(
            _known_bool(
                "perspective_consistency",
                route_count > 0 and composition_residual <= tol,
                ("three_clock_route_count", "max_cross_clock_composition_residual"),
                "The witness contains genuine distinct-clock routes whose composition residual is within tolerance.",
            ),
            _known_bool(
                "physical_clock_change",
                route_count > 0,
                ("three_clock_route_count",),
                "The Stage 5 route count enumerates ordered distinct physical-clock routes.",
            ),
            _known_bool(
                "perspective_dependent_structure",
                perspective_dependent,
                (
                    "entanglement_perspective_dependent",
                    "entanglement_A_bits",
                    "entanglement_B_bits",
                    "entanglement_C_bits",
                ),
            ),
            _known_bool(
                "operational_inconsistency",
                born_residual > tol,
                ("max_born_probability_residual",),
                "A residual within tolerance is an executable false value for operational inconsistency.",
            ),
            _unknown(
                "temporal_arrow_present",
                "Cross-clock consistency is a horizontal perspective property, not an explicit temporal-arrow measurement.",
            ),
            _unknown(
                "temporal_succession",
                "The Stage 5 clock-change witness does not measure cross-perspective temporal succession.",
            ),
            _unknown(
                "modal_ontological_equivalence",
                "The Stage 5 witness carries no modal-semantics comparison.",
            ),
        ),
    )


def build_stage6b_cases(
    inventory: Iterable[WitnessRecord] | None = None,
) -> tuple[EvidenceCase, ...]:
    """Expand W1--W5 into measurement-backed Stage 6B evidence cases."""

    records = tuple(build_stage6a_inventory() if inventory is None else inventory)
    by_id = {record.witness_id: record for record in records}
    if len(by_id) != len(records):
        raise ValueError("Stage 6B inventory contains duplicate witness IDs")

    cases: list[EvidenceCase] = []
    if "W1" in by_id:
        cases.append(_w1_case(by_id["W1"]))
    if "W2" in by_id:
        cases.append(_w2_case(by_id["W2"]))
    if "W3" in by_id:
        cases.extend(_w3_cases(by_id["W3"]))
    if "W4" in by_id:
        cases.append(_w4_case(by_id["W4"]))
    if "W5" in by_id:
        cases.append(_w5_case(by_id["W5"]))
    return tuple(cases)


def assess_implication(
    spec: ImplicationSpec,
    cases: Iterable[EvidenceCase],
) -> ImplicationAssessment:
    """Classify one implication from case facts rather than a fixed answer table."""

    evidence: list[CaseEvidence] = []
    for case in cases:
        antecedent = case.fact(spec.antecedent)
        if antecedent.value is not TruthValue.TRUE:
            continue
        evidence.append(
            CaseEvidence(
                case_id=case.case_id,
                witness_id=case.witness_id,
                antecedent=antecedent,
                consequent=case.fact(spec.consequent),
            )
        )

    has_countermodel = any(
        item.consequent.value is TruthValue.FALSE for item in evidence
    )
    has_unknown = any(
        item.consequent.value is TruthValue.UNKNOWN for item in evidence
    )

    if has_countermodel:
        status = ImplicationStatus.REFUTED
    elif evidence and not has_unknown:
        status = ImplicationStatus.SUPPORTED_IN_DECLARED_FAMILY
    else:
        status = ImplicationStatus.NOT_ESTABLISHED

    return ImplicationAssessment(spec=spec, status=status, evidence=tuple(evidence))


def build_stage6b_matrix(
    inventory: Iterable[WitnessRecord] | None = None,
) -> tuple[ImplicationAssessment, ...]:
    """Evaluate the complete frozen ten-implication Stage 6B matrix."""

    cases = build_stage6b_cases(inventory)
    return tuple(assess_implication(spec, cases) for spec in FROZEN_IMPLICATIONS)


def stage6b_case_rows(
    inventory: Iterable[WitnessRecord] | None = None,
) -> tuple[dict[str, Any], ...]:
    """Return JSON-friendly evidence cases."""

    return tuple(case.as_dict() for case in build_stage6b_cases(inventory))


def stage6b_matrix_rows(
    inventory: Iterable[WitnessRecord] | None = None,
) -> tuple[dict[str, Any], ...]:
    """Return JSON-friendly implication assessments with measurement provenance."""

    return tuple(item.as_dict() for item in build_stage6b_matrix(inventory))

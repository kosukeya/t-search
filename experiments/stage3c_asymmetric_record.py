"""Stage 3C canonical asymmetric-record assessment."""

from t_search.stage3_asymmetry import canonical_record_orientation_assessment


def main() -> None:
    assessment = canonical_record_orientation_assessment()

    print("Stage 3C — asymmetric-record model")
    print("order != arrow")
    print("record-defined orientation != fundamental temporal arrow")
    print()
    print("neutral comparison positions:", assessment.lower_position, assessment.upper_position)
    print("I(M1;X0):", assessment.lower_information)
    print("I(M1;X2):", assessment.upper_information)
    print("Acc(M1->X0):", assessment.lower_accuracy)
    print("Acc(M1->X2):", assessment.upper_accuracy)
    print("A_R:", assessment.record_score)
    print("A_Acc:", assessment.accessibility_score)
    print("diagnostics agree:", assessment.diagnostics_agree)
    print("orientation:", assessment.orientation)
    print("record-defined:", assessment.record_defined)
    print("microscopic maps reversible:", assessment.microscopic_maps_reversible)


if __name__ == "__main__":
    main()

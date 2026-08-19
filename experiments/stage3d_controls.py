"""Stage 3D experiment: compare reversal, symmetric, no-record, and boundary controls."""

from t_search.stage3_controls import stage3d_control_assessments


def main() -> None:
    print("Stage 3D — reversal and symmetric controls")
    print("simulation order != modeled temporal order")
    print("record-defined orientation != fundamental temporal arrow")
    print()

    assessments = stage3d_control_assessments()
    for name, assessment in assessments.items():
        print(name)
        print(f"  lower information: {assessment.lower_information:.12f}")
        print(f"  upper information: {assessment.upper_information:.12f}")
        print(f"  lower accuracy: {assessment.lower_accuracy:.12f}")
        print(f"  upper accuracy: {assessment.upper_accuracy:.12f}")
        print(f"  A_R: {assessment.record_score:.12f}")
        print(f"  A_Acc: {assessment.accessibility_score:.12f}")
        print(f"  orientation: {assessment.orientation}")
        print(f"  record-defined: {assessment.record_defined}")
        print()


if __name__ == "__main__":
    main()

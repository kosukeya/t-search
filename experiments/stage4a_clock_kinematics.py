"""Report residuals for the Stage 4A finite clock."""

import numpy as np

from t_search.stage4_quantum import (
    canonical_stage4a_kinematics,
    clock_gram_matrix,
    clock_state,
    clock_translation_unitary,
    translate_clock_state,
)


def main() -> None:
    fixture = canonical_stage4a_kinematics()
    d = fixture.dimension
    eye = np.eye(d, dtype=np.complex128)
    gram_error = np.max(np.abs(clock_gram_matrix(d) - eye))
    step_error = max(
        np.max(
            np.abs(
                translate_clock_state(clock_state(j, d), d)
                - clock_state((j + 1) % d, d)
            )
        )
        for j in range(d)
    )
    period_error = np.max(np.abs(clock_translation_unitary(d, steps=d) - eye))

    print("Stage 4A — finite clock kinematics")
    print("kinematic dimension:", fixture.kinematic_dimension)
    print("clock readings:", fixture.clock_times)
    print("Gram residual:", float(gram_error))
    print("one-step residual:", float(step_error))
    print("full-period residual:", float(period_error))
    print("Page-Wootters physical-dynamics claim: none at Stage 4A")


if __name__ == "__main__":
    main()

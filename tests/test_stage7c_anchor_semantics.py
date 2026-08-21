import numpy as np

from t_search.stage5_clock_change import clock_state
from t_search.stage5_reductions import clock_relative_support_pairs
from t_search.stage7_history import (
    history_dressing_operator,
    pair_scrambler_support_matrix,
    schedule_rest_operators,
)

ATOL = 1e-10


def _coordinate(pair_index: int, memory_bit: int, pair_count: int = 7) -> np.ndarray:
    vector = np.zeros(pair_count * 2, dtype=np.complex128)
    vector[pair_index * 2 + memory_bit] = 1.0
    return vector


def test_stage7c_scrambler_implements_x_xor_n_not_unconditional_bit_flip():
    pairs = clock_relative_support_pairs("A")
    u = pair_scrambler_support_matrix()
    for memory_bit in (0, 1):
        # N=0 (C=0): X is unchanged.
        for pair in ((-1, 0), (0, 0)):
            source = _coordinate(pairs.index(pair), memory_bit)
            assert np.allclose(u @ source, source, atol=ATOL, rtol=0.0)

        # N=1 (C=+1): X toggles between B=-1 and B=0.
        first = _coordinate(pairs.index((-1, 1)), memory_bit)
        second = _coordinate(pairs.index((0, 1)), memory_bit)
        assert np.allclose(u @ first, second, atol=ATOL, rtol=0.0)
        assert np.allclose(u @ second, first, atol=ATOL, rtol=0.0)


def test_stage7c_global_dressing_applies_declared_vj_at_each_internal_clock_reading():
    dressing = history_dressing_operator("forward")
    schedule = schedule_rest_operators("forward")
    raw = np.arange(1, 19, dtype=float) + 1j * np.arange(18, 0, -1, dtype=float)
    rest = raw.astype(np.complex128) / np.linalg.norm(raw)

    for index, v_j in enumerate(schedule):
        clock = clock_state(index, 3, rate=1.0)
        global_input = np.kron(clock, rest)
        expected = np.kron(clock, v_j @ rest)
        assert np.allclose(dressing @ global_input, expected, atol=ATOL, rtol=0.0)

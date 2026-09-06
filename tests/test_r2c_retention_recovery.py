"""Independent channel, classical-probability, and reference-state oracles."""
import hashlib
import itertools
import json
from pathlib import Path
import runpy
import unittest
import numpy as np

ROOT = Path(__file__).resolve().parents[1]
M = runpy.run_path(str(ROOT/"experiments/r2c_retention_recovery.py"))
B = M["B"]
ATOL = 1e-10


def unpack(data):
    a = np.zeros((data["dimension"], data["dimension"]), complex)
    for i, j, real, imag in data["entries"]:
        a[i, j] = real+1j*imag
    return a


class RetentionRecoveryTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.report = M["run_experiment"]()

    def close(self, a, b):
        np.testing.assert_allclose(a, b, atol=ATOL, rtol=0)

    def test_noise_on_full_operator_basis(self):
        # Independent index-level bit-flip action, no Kraus construction reused.
        for p in M["PROBABILITIES"]:
            ops = M["noise_kraus"](p)
            for row, col in itertools.product(range(16), repeat=2):
                unit = np.zeros((16, 16), complex)
                unit[row, col] = 1
                expected = np.zeros_like(unit)
                for i, j in itertools.product((0, 1), repeat=2):
                    mask = 4*i+2*j
                    expected[row ^ mask, col ^ mask] += (p if i else 1-p)*(p if j else 1-p)
                self.close(M["apply_kraus"](unit, ops), expected)

    def test_cptp_completeness_on_entire_access_spaces(self):
        for p in M["PROBABILITIES"]:
            self.close(M["tp_residual"](M["noise_kraus"](p)), 0)
        for condition, scope in itertools.product(B["CONDITIONS"], M["SCOPES"]):
            for family in ("encoding_kraus", "decoder_kraus", "composite_kraus"):
                self.close(M["tp_residual"](M[family](condition, scope)), 0)

    def test_retention_joint_probabilities_against_classical_oracle(self):
        for row in self.report["retention_cases"]:
            p = row["p"]
            expected = np.zeros((2, 2, 2))
            for b, x, y in itertools.product((0, 1), repeat=3):
                record = 0 if row["condition"] == "no_record" else b
                expected[b, x, y] = .5*(1-p if x == record else p)*(1-p if y == record else p)
            self.close(row["joint_probabilities"], expected)
            e = .5 if row["condition"] == "no_record" else p
            self.close(row["errors"], [e, e])
            self.close(row["agreement"], 1-2*p+2*p*p)
            self.close(row["both_correct"], (1-2*p+2*p*p)/2 if row["condition"] == "no_record" else (1-p)**2)

    def test_noise_is_medium_update_and_leaves_s_e_marginal(self):
        for condition in B["CONDITIONS"]:
            state = B["encode"](B["inputs"]()["plus_i"], condition)
            for p in M["PROBABILITIES"]:
                post = M["apply_kraus"](state, M["noise_kraus"](p))
                self.close(B["marginal"](post, (0, 3)), B["marginal"](state, (0, 3)))
        state = B["encode"](np.diag([1, 0]), "records_E_on")
        self.assertGreater(B["distance"](state, M["apply_kraus"](state, M["noise_kraus"](.5))), .1)

    def test_encoding_channels_against_basis_images(self):
        for condition, scope in itertools.product(B["CONDITIONS"], M["SCOPES"]):
            dimension = 8 if scope == "Q" else 16
            index = {("no_record", "Q"): (0, 4), ("no_record", "G"): (0, 8),
                     ("records_E_off", "Q"): (0, 7), ("records_E_off", "G"): (0, 14),
                     ("records_E_on", "Q"): (0, 7), ("records_E_on", "G"): (0, 15)}[(condition, scope)]
            for i, j in itertools.product((0, 1), repeat=2):
                unit = np.zeros((2, 2), complex)
                unit[i, j] = 1
                expected = np.zeros((dimension, dimension), complex)
                if not (condition == "records_E_on" and scope == "Q" and i != j):
                    expected[index[i], index[j]] = 1
                self.close(M["apply_kraus"](unit, M["encoding_kraus"](condition, scope)), expected)

    def test_recovered_channels_on_complete_input_operator_basis(self):
        for condition, scope in itertools.product(B["CONDITIONS"], M["SCOPES"]):
            for i, j in itertools.product((0, 1), repeat=2):
                unit = np.zeros((2, 2), complex)
                unit[i, j] = 1
                expected = np.diag(np.diag(unit)) if (condition == "records_E_on" and scope == "Q") else unit
                self.close(M["apply_kraus"](unit, M["composite_kraus"](condition, scope)), expected)

    def test_reference_states_and_optimal_bound_attainment(self):
        bell = np.zeros((4, 4), complex)
        bell[np.ix_([0, 3], [0, 3])] = .5
        classical = np.diag([.5, 0, 0, .5])
        for row in self.report["recovery_cases"]:
            dephased = row["condition"] == "records_E_on" and row["scope"] == "Q"
            self.close(unpack(row["recovered_reference_state"]), classical if dephased else bell)
            self.close(row["achieved_entanglement_fidelity"], .5 if dephased else 1)
            self.close(row["upper_bound_gap"], 0)

    def test_reference_route_by_unitary_then_partial_trace(self):
        # Check reference handling by a distinct Stinespring route, keeping E until access is restricted.
        phi = np.array([1, 0, 0, 1], complex)/np.sqrt(2)
        for condition, scope in itertools.product(B["CONDITIONS"], M["SCOPES"]):
            v = np.kron(np.eye(2), B["encoding"](condition))
            total = np.outer(v @ phi, (v @ phi).conj())
            if scope == "Q":
                # Trace the last (E) axis explicitly, without the production marginal helper.
                total = np.trace(total.reshape(16, 2, 16, 2), axis1=1, axis2=3)
            u = np.kron(np.eye(2), M["decoder_unitary"](condition, scope))
            decoded = u @ total @ u.conj().T
            ancillary_dimension = decoded.shape[0]//4
            rs = np.trace(decoded.reshape(4, ancillary_dimension, 4, ancillary_dimension), axis1=1, axis2=3)
            self.close(rs, M["reference_output"](M["composite_kraus"](condition, scope)))

    def test_phase_collision_is_only_restricted_e_on_case(self):
        for row in self.report["recovery_cases"]:
            collision = row["condition"] == "records_E_on" and row["scope"] == "Q"
            self.close(row["phase_pair_input_distance"], 1)
            self.close(row["phase_pair_accessible_distance"], 0 if collision else 1)

    def test_known_state_repreparation_does_not_pass_reference_test(self):
        plus = np.array([1, 1], complex)/np.sqrt(2)
        replacement = [np.outer(plus, basis) for basis in np.eye(2)]
        self.close(M["tp_residual"](replacement), 0)
        self.close(M["apply_kraus"](np.outer(plus, plus.conj()), replacement), np.outer(plus, plus.conj()))
        # Perfect for this known input, but Fe=1/4 rather than one.
        self.close(np.trace(M["bell_state"]() @ M["reference_output"](replacement)), .25)

    def test_validity_and_rejection_without_repair(self):
        def walk(value):
            if isinstance(value, dict):
                for key, item in value.items():
                    if key == "minimum_eigenvalue":
                        self.assertGreaterEqual(item, -ATOL)
                    elif key.endswith("_residual_fro") or key in (
                            "trace_error", "normalization_error", "analytic_max_error"):
                        self.assertLessEqual(item, ATOL)
                    else:
                        walk(item)
            elif isinstance(value, list):
                for item in value:
                    walk(item)
        walk(self.report)
        for p in (-.1, 1.1, np.nan, np.inf):
            with self.assertRaises(ValueError):
                M["noise_kraus"](p)
        with self.assertRaises(ValueError):
            M["encoding_kraus"]("records_E_on", "F1")

    def test_saved_results_and_source_hashes(self):
        saved = json.loads((ROOT/"results/r2c_retention_recovery.json").read_text())
        self.assertEqual(saved["summary"]["retention_case_count"], 12)
        self.assertEqual(saved["summary"]["recovery_case_count"], 6)
        for path, digest in saved["provenance"]["source_sha256"].items():
            self.assertEqual(hashlib.sha256((ROOT/path).read_bytes()).hexdigest(), digest)
        def compare(a, b):
            if isinstance(a, dict):
                self.assertEqual(set(a), set(b))
                for key in a:
                    compare(a[key], b[key])
            elif isinstance(a, list):
                self.assertEqual(len(a), len(b))
                for x, y in zip(a, b):
                    compare(x, y)
            elif isinstance(a, (int, float)) and not isinstance(a, bool):
                self.close(a, b)
            else:
                self.assertEqual(a, b)
        compare({k:v for k,v in saved.items() if k != "provenance"},
                {k:v for k,v in self.report.items() if k != "provenance"})


if __name__ == "__main__":
    unittest.main()

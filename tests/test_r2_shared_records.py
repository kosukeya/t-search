"""Independent analytic oracles for R2b; unittest also runs under normal pytest."""
import hashlib
import itertools
import json
from pathlib import Path
import runpy
import unittest
import numpy as np

ROOT = Path(__file__).resolve().parents[1]
M = runpy.run_path(str(ROOT/"experiments/r2_shared_records.py"))
ATOL = 1e-10


def unpack(data):
    a = np.zeros((data["dimension"], data["dimension"]), complex)
    for i, j, real, imag in data["entries"]:
        a[i, j] = real+1j*imag
    return a


def analytic_state(rho, condition):
    # Fixed basis images derived in the specification, not from the circuit.
    indices = {"no_record": (0, 8), "records_E_off": (0, 14),
               "records_E_on": (0, 15)}[condition]
    a = np.zeros((16, 16), complex)
    for b, d in itertools.product((0, 1), repeat=2):
        a[indices[b], indices[d]] = rho[b, d]
    return a


class SharedRecordsTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.report = M["run_experiment"]()

    def close(self, a, b):
        np.testing.assert_allclose(a, b, atol=ATOL, rtol=0)

    def test_cnot_on_entire_computational_basis(self):
        for target in (1, 2, 3):
            u = M["cnot"](target)
            for bits in itertools.product((0, 1), repeat=4):
                out = list(bits)
                out[target] = bits[target] ^ bits[0]
                col = int(''.join(map(str, bits)), 2)
                row = int(''.join(map(str, out)), 2)
                self.close(u[:, col], np.eye(16)[:, row])

    def test_encoding_and_complex_coherences(self):
        for condition in M["CONDITIONS"]:
            v = M["encoding"](condition)
            self.close(v.conj().T @ v, np.eye(2))
            for name, rho in M["inputs"]().items():
                with self.subTest(condition=condition, input=name):
                    self.close(M["encode"](rho, condition), analytic_state(rho, condition))

    def test_partial_trace_independent_index_sum(self):
        matrix = np.arange(256).reshape(16, 16)+1j*np.arange(256)[::-1].reshape(16, 16)
        for keep in ((0,), (0, 1, 2), (1, 3), (), (0, 1, 2, 3)):
            expected = np.zeros((2**len(keep), 2**len(keep)), complex)
            for i, j in itertools.product(range(16), repeat=2):
                bi = tuple(map(int, f'{i:04b}'))
                bj = tuple(map(int, f'{j:04b}'))
                if all(bi[k] == bj[k] for k in range(4) if k not in keep):
                    ii = sum(bi[k]*2**(len(keep)-1-pos) for pos, k in enumerate(keep))
                    jj = sum(bj[k]*2**(len(keep)-1-pos) for pos, k in enumerate(keep))
                    expected[ii, jj] += matrix[i, j]
            self.close(M["marginal"](matrix, keep), expected)

    def test_instrument_completeness_and_effect_bounds(self):
        for readout in M["READOUTS"]:
            ops = [p for _, p in M["readout_kraus"](readout)]
            self.close(sum(p.conj().T @ p for p in ops), np.eye(16))
            for i, p in enumerate(ops):
                self.close(p, p.conj().T)
                self.close(p @ p, p)
                self.assertGreaterEqual(np.linalg.eigvalsh(np.eye(16)-p.conj().T @ p).min(), -ATOL)
                for j, q in enumerate(ops):
                    if i != j:
                        self.close(p @ q, np.zeros((16, 16)))

    def test_exact_calibration_and_uninformative_agreement(self):
        for condition, row in self.report["calibration"].items():
            expected = np.zeros((2, 2, 2))
            expected[0, 0, 0] = .5
            if condition == "no_record":
                expected[1, 0, 0] = .5
                self.close(row["errors"], [.5, .5])
            else:
                expected[1, 1, 1] = .5
                self.close(row["errors"], [0, 0])
            self.close(row["joint_probabilities"], expected)
            self.close(row["agreement"], 1)

    def test_post_states_and_distances_against_analytic_oracles(self):
        for row in self.report["cases"]:
            condition = row["condition"]
            rho = unpack(row["input_state"])
            expected_before = analytic_state(rho, condition)
            # Reading F removes only the cross-branch terms in recorded cases.
            expected_after = analytic_state(rho if condition == "no_record" else
                                            np.diag(np.diag(rho)), condition)
            self.close(unpack(row["before_states"]["G"]), expected_before)
            for result in row["readouts"]:
                self.close(unpack(result["nonselective_state"]), expected_after)
                for scope in ("S", "Q", "G"):
                    expected_d = 0 if (condition == "no_record" or scope == "S" or
                        (condition == "records_E_on" and scope == "Q")) else abs(rho[0, 1])
                    self.close(result["disturbance"][scope]["trace_distance"], expected_d)

    def test_trace_norm_not_frobenius(self):
        a = np.diag([.5, .5, 0, 0])
        b = np.diag([0, 0, .5, .5])
        self.close(M["distance"](a, b), 1)

    def test_all_branches_roundtrip_and_selective_repeatability(self):
        for row in self.report["cases"]:
            for result in row["readouts"]:
                readout = tuple(result["fragments"])
                total = np.zeros((16, 16), complex)
                probability_sum = 0
                for branch in result["branches"]:
                    p = branch["probability"]
                    probability_sum += p
                    if p == 0:
                        self.assertIsNone(branch["conditional_state"])
                        self.assertEqual(branch["undefined_reason"], "zero probability")
                    else:
                        state = unpack(branch["conditional_state"])
                        total += p*state
                        self.close(np.trace(state), 1)
                        for outcome, repeated in M["instrument"](state, readout):
                            self.close(np.trace(repeated), int(list(outcome) == branch["outcome"]))
                self.close(probability_sum, 1)
                self.close(total, unpack(result["nonselective_state"]))

    def test_tiny_positive_branch_not_discarded(self):
        rho = np.diag([1-1e-12, 1e-12])
        omega = M["encode"](rho, "records_E_on")
        branch = M["instrument"](omega, (1,))[1][1]
        self.assertGreater(np.trace(branch).real, 0)
        self.close(np.trace(branch/np.trace(branch)), 1)
        structure = M["fixed_z_sbs"](omega)
        self.assertIsNotNone(structure["support_product_residuals_fro"])

    def test_fixed_basis_sbs_scope_and_degenerate_inputs(self):
        for row in self.report["cases"]:
            condition, name = row["condition"], row["input"]
            rho = unpack(row["input_state"])
            if name in ("zero", "one"):
                for scope in ("Q", "G"):
                    self.assertTrue(row["fixed_z_sbs"][scope]["fixed_z_structure_satisfied"])
                    self.assertIn("vacuous", row["fixed_z_sbs"][scope]["support_check_note"])
            else:
                expected_q = condition == "records_E_on" or (
                    condition == "records_E_off" and rho[0, 1] == 0)
                expected_g = condition == "records_E_on" and rho[0, 1] == 0
                self.assertEqual(row["fixed_z_sbs"]["Q"]["fixed_z_structure_satisfied"], expected_q)
                self.assertEqual(row["fixed_z_sbs"]["G"]["fixed_z_structure_satisfied"], expected_g)

    def test_sbs_rejects_conditional_correlations_and_overlapping_records(self):
        bell = np.array([1, 0, 0, 1])/np.sqrt(2)
        state = np.kron(np.diag([1, 0]), np.outer(bell, bell))
        result = M["fixed_z_sbs"](state)
        self.assertGreater(result["conditional_product_residuals_fro"][0], .1)
        self.assertFalse(result["fixed_z_structure_satisfied"])
        fixed_records = np.kron(np.eye(2)/2, np.diag([1, 0, 0, 0]))
        result = M["fixed_z_sbs"](fixed_records)
        self.close(result["support_product_residuals_fro"], [1, 1])
        self.assertFalse(result["fixed_z_structure_satisfied"])

    def test_numerical_validity_and_order(self):
        def visit(value):
            if isinstance(value, dict):
                for key, item in value.items():
                    if key == "minimum_eigenvalue":
                        self.assertGreaterEqual(item, -ATOL)
                    elif key in (
                            "unitarity_residual_fro", "isometry_residual_fro",
                            "tp_completeness_residual_fro", "projector_residual_fro",
                            "hermitian_residual_fro", "recomposition_residual_fro",
                            "repeat_nonselective_residual_fro", "readout_order_residual_fro",
                            "trace_error", "probability_sum_error", "absolute_error"):
                        self.assertLessEqual(item, ATOL)
                    else:
                        visit(item)
            elif isinstance(value, list):
                for item in value:
                    visit(item)
        visit(self.report)
        self.assertEqual(self.report["summary"]["case_count"], 18)
        self.assertEqual(self.report["summary"]["readout_comparisons"], 54)

    def test_invalid_inputs_are_rejected_not_repaired(self):
        invalid = [np.eye(2), np.diag([1.1, -.1]), np.array([[.5, .1j], [.1j, .5]]),
                   np.full((2, 2), np.nan), np.eye(3)/3]
        for rho in invalid:
            with self.assertRaises(ValueError):
                M["encode"](rho, "records_E_on")

    def test_committed_result_and_source_provenance(self):
        saved = json.loads((ROOT/"results/r2_shared_records.json").read_text())
        for path, digest in saved["provenance"]["source_sha256"].items():
            self.assertEqual(hashlib.sha256((ROOT/path).read_bytes()).hexdigest(), digest)
        # Python/NumPy version strings may differ on CI; scientific payload must agree.
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
        compare({k: v for k, v in saved.items() if k != "provenance"},
                {k: v for k, v in self.report.items() if k != "provenance"})


if __name__ == "__main__":
    unittest.main()

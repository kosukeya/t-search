"""Independent algebra, phase-sensitive controls and saved R5b evidence."""
import hashlib
import itertools
import json
from pathlib import Path
import runpy
import unittest

import numpy as np

ROOT = Path(__file__).resolve().parents[1]
E = runpy.run_path(str(ROOT / "experiments/r5b_record_stability.py"))


class RecordStabilityTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.report = E["run_experiment"]()
        cls.rows = {(r["angle"], r["input"]): r for r in cls.report["cases"]}

    def close(self, a, b):
        np.testing.assert_allclose(a, b, atol=1e-10, rtol=0)

    def test_gate_on_entire_basis_and_exact_endpoint_operations(self):
        for _, theta in E["ANGLES"]:
            u = E["environment_gate"](theta)
            a, b = (1+np.exp(2j*theta))/2, (1-np.exp(2j*theta))/2
            for col in range(16):
                want = np.zeros(16, complex)
                if col & 4:  # F1, not S, controls E
                    want[col], want[col ^ 1] = a, b
                else:
                    want[col] = 1
                self.close(u[:, col], want)
            self.close(u.conj().T @ u, np.eye(16))
        self.close(E["environment_gate"](0), np.eye(16))
        self.close(E["environment_gate"](np.pi/2), E["cnot"](1, 3))
        self.assertFalse(np.allclose(E["environment_gate"](np.pi/2), E["cnot"](0, 3)))

    def test_encoding_and_partial_trace_on_full_input_operator_basis(self):
        for _, theta in E["ANGLES"]:
            w = E["embedding"](theta)
            v0, v1 = np.eye(16, dtype=complex)[:, 0], np.zeros(16, complex)
            v1[12], v1[13] = (1+np.exp(2j*theta))/2, (1-np.exp(2j*theta))/2
            vectors = (v0, v1)
            gamma = np.exp(1j*theta)*np.cos(theta)
            for i, j in itertools.product((0, 1), repeat=2):
                op = np.zeros((2, 2), complex)
                op[i, j] = 1
                g = w @ op @ w.conj().T
                self.close(g, np.outer(vectors[i], vectors[j].conj()))
                expected_q = np.zeros((8, 8), complex)
                expected_q[6*i, 6*j] = 1 if i == j else (gamma.conjugate() if i == 0 else gamma)
                self.close(E["marginal"](g, (0, 1, 2)), expected_q)
            self.close(w.conj().T @ w, np.eye(2))

    def test_dephasing_full_operator_basis_preserves_within_branch_coherence(self):
        ps = E["pointer_projectors"]()
        self.close(sum(p.conj().T @ p for p in ps), np.eye(16))
        for i, j in itertools.product(range(16), repeat=2):
            op = np.zeros((16, 16), complex)
            op[i, j] = 1
            self.close(E["dephase"](op), op if (i & 4) == (j & 4) else np.zeros_like(op))
        r = self.rows["pi/4", "one"]
        gd = E["unpack"](r["states"]["dephased_G"])
        self.assertGreater(abs(gd[12, 13]), .49)
        self.close(gd, E["unpack"](r["states"]["rho_G"]))

    def test_readouts_are_complete_and_do_not_access_environment(self):
        for measurements in (E["pointer_measurement"](), E["undo_x_measurement"]()):
            self.close(sum(measurements), np.eye(16))
            for m in measurements:
                self.close(m @ m, m)
                q = m.reshape(8, 2, 8, 2)[:, 0, :, 0]
                self.close(m, np.kron(q, np.eye(2)))
        for r in self.report["cases"]:
            for key, n in (("pointer_readout", 4), ("undo_x_readout", 2)):
                for side in ("quantum", "dephased"):
                    p = r[key][side]
                    self.assertEqual(len(p), n)
                    self.close(sum(p), 1)
                    self.assertGreaterEqual(min(p), -1e-10)

    def test_all_fixed_distances_and_density_matrices(self):
        self.assertEqual(len(self.rows), 25)
        for label, theta in E["ANGLES"]:
            for name in E["probes"]():
                r = self.rows[label, name]
                coherence = .5 if name in ("plus", "plus_i") else 0.
                self.close([r["distances"][k] for k in ("C_Z", "C_Q", "C_G")],
                           [0, coherence*np.cos(theta), coherence])
                for data in r["states"].values():
                    state = E["unpack"](data)
                    self.close(state, state.conj().T)
                    self.close(np.trace(state), 1)
                    self.assertGreaterEqual(np.linalg.eigvalsh(state).min(), -1e-10)

    def test_phase_sensitive_x_probabilities_and_blind_measurement(self):
        for label, theta in E["ANGLES"]:
            plus = self.rows[label, "plus"]["undo_x_readout"]
            plus_i = self.rows[label, "plus_i"]["undo_x_readout"]
            self.close(plus["quantum"], [.5+np.cos(theta)**2/2, .5-np.cos(theta)**2/2])
            signed = -np.sin(theta)*np.cos(theta)/2
            self.close(plus_i["quantum"], [.5+signed, .5-signed])
            self.close(plus_i["dephased"], [.5, .5])
            self.close(plus["dephased"], [.5, .5])
        blind = self.rows["0", "plus_i"]
        self.close(blind["undo_x_readout"]["total_variation"], 0)
        self.close(blind["distances"]["C_Q"], .5)
        # The controlled global phase of V is observable between F1 branches.
        gamma = complex(*self.rows["pi/4", "plus"]["gamma"])
        self.close(gamma, .5+.5j)
        self.assertGreater(abs(gamma.imag), .49)

    def test_record_calibration_is_separate_from_predictive_distance(self):
        for r in self.report["calibration_summary"]:
            self.close([r["F1_correct"], r["F2_correct"]], [1, .5])
        for label, _ in E["ANGLES"]:
            for name in ("plus", "plus_i", "maximally_mixed"):
                self.assertIsNone(self.rows[label, name]["calibration"])
        negative = self.report["no_record_control"]
        self.close(negative["F1_correct"], .5)
        self.assertEqual(len(negative["cases"]), 2)
        for r in negative["cases"]:
            self.close(list(r["distances"].values()), [0, 0, 0])
            self.close(r["pointer_readout"]["quantum"], [1, 0, 0, 0])

    def test_full_r4_endpoint_fixture_and_terminal_formula(self):
        old = json.loads((ROOT / E["REFERENCE_PATH"]).read_text())
        oldrows = {(r["context"], r["environment"], r["input"]): r for r in old["cases"]}
        seen = set()
        for r in self.report["endpoint_checks"]:
            key = (r["context"], r["environment"], r["input"])
            self.assertNotIn(key, seen)
            seen.add(key)
            self.close(E["unpack"](r["event2_state_G"]), E["unpack"](oldrows[key]["events"][2]["state_G"]))
            self.close(r["terminal_probabilities"], oldrows[key]["terminal_probabilities"])
            rho = E["probes"]()[r["input"]]
            expected = []
            for s, f, g in itertools.product((1, -1), (0, 1), (0, 1)):
                if r["context"] == "read":
                    value = rho[f, f].real/2 if f == g else 0
                elif r["context"] == "undo":
                    value = .5+s*rho[0, 1].real*(1-r["environment"]) if (f, g) == (0, 0) else 0
                else:
                    value = rho[g, g].real/2 if f == 0 else 0
                expected.append(value)
            self.close(r["terminal_probabilities"], expected)
        self.assertEqual(seen, set(oldrows))
        self.assertEqual(len(seen), 24)

    def test_invalid_parameters_and_nonstates_are_rejected(self):
        for theta in (-.01, np.pi, float("nan"), float("inf"), 1j, [0]):
            with self.assertRaises(ValueError):
                E["environment_gate"](theta)
        for rho in (np.eye(2), np.diag([2, -1]), np.array([[1, 1], [0, 0]]),
                    np.full((2, 2), np.nan), np.eye(3)/3):
            with self.assertRaises(ValueError):
                E["case"]("0", 0, "invalid", rho)

    def test_saved_evidence_and_provenance(self):
        self.assertTrue(self.report["summary"]["all_checks_within_tolerance"])
        saved = json.loads((ROOT / "results/r5b_record_stability.json").read_text())
        for group in ("source_sha256", "reference_sha256"):
            for path, digest in saved["provenance"][group].items():
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
            elif isinstance(a, bool):
                self.assertIs(a, b)
            elif isinstance(a, (int, float)):
                self.close(a, b)
            else:
                self.assertEqual(a, b)
        compare({k: v for k, v in saved.items() if k != "provenance"},
                {k: v for k, v in self.report.items() if k != "provenance"})


if __name__ == "__main__":
    unittest.main()

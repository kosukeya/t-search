"""Independent support algebra, gate actions and saved R5c evidence."""
import hashlib
import itertools
import json
from pathlib import Path
import runpy
import unittest

import numpy as np

ROOT = Path(__file__).resolve().parents[1]
E = runpy.run_path(str(ROOT / "experiments/r5c_access_guarantees.py"))
B = E["B"]


class AccessGuaranteeTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.report = E["run_experiment"]()
        cls.rows = {(r["angle"], r["input"]): r for r in cls.report["cases"]}

    def close(self, a, b):
        np.testing.assert_allclose(a, b, atol=1e-10, rtol=0)

    def test_decoders_on_every_computational_basis_vector(self):
        undo = np.zeros((16, 16), complex)
        for col in range(16):
            undo[col ^ 4 if col & 8 else col, col] = 1
        for _, theta in B["ANGLES"]:
            inverse_env = np.zeros((16, 16), complex)
            a, b = (1+np.exp(-2j*theta))/2, (1-np.exp(-2j*theta))/2
            for col in range(16):
                if col & 4:
                    inverse_env[col, col], inverse_env[col ^ 1, col] = a, b
                else:
                    inverse_env[col, col] = 1
            self.close(E["decoder"](theta, "Q"), undo)
            self.close(E["decoder"](theta, "G"), undo @ inverse_env)
            for scope in ("Q", "G"):
                d = E["decoder"](theta, scope)
                self.close(d.conj().T @ d, np.eye(16))

    def test_global_decode_and_dephased_control_on_full_input_operator_basis(self):
        for _, theta in B["ANGLES"]:
            w = B["embedding"](theta)
            d = E["decoder"](theta, "G")
            for i, j in itertools.product((0, 1), repeat=2):
                op = np.zeros((2, 2), complex)
                op[i, j] = 1
                g = w @ op @ w.conj().T
                expected = np.zeros((16, 16), complex)
                expected[8*i, 8*j] = 1
                self.close(d @ g @ d.conj().T, expected)
                self.close(d @ B["dephase"](g) @ d.conj().T,
                           expected if i == j else np.zeros((16, 16)))
        # The decoder has erased F1 even for a prepared input of one.
        self.close(E["decoder"](np.pi/2, "G") @ B["embedding"](np.pi/2)[:, 1],
                   np.eye(16)[:, 8])

    def test_circuit_measurements_against_independent_support_formula(self):
        for _, theta in B["ANGLES"]:
            gamma = (1+np.exp(2j*theta))/2
            w = B["embedding"](theta)
            for phi in (0., np.pi/2, -np.pi/2, .37):
                for scope, overlap in (("Q", gamma), ("G", 1.)):
                    m, _ = E["readout"](theta, scope, phi)
                    target = np.array([[.5, overlap*np.exp(-1j*phi)/2],
                                       [np.conjugate(overlap)*np.exp(1j*phi)/2, .5]])
                    self.close(w.conj().T @ m[0] @ w, target)
                    self.close(w.conj().T @ m[1] @ w, np.eye(2)-target)

    def test_full_space_completeness_and_environment_access(self):
        for scope in ("Q", "G"):
            for _, theta in B["ANGLES"]:
                m, u = E["readout"](theta, scope, -.71)
                self.close(sum(m), np.eye(16))
                self.close(u.conj().T @ u, np.eye(16))
                for effect in m:
                    self.close(effect, effect.conj().T)
                    self.close(effect @ effect, effect)
                    self.assertGreaterEqual(np.linalg.eigvalsh(effect).min(), -1e-10)
                    local = effect.reshape(8, 2, 8, 2)[:, 0, :, 0]
                    if scope == "Q":
                        self.close(effect, np.kron(local, np.eye(2)))
        m, _ = E["readout"](np.pi/2, "G", 0.)
        local = m[0].reshape(8, 2, 8, 2)[:, 0, :, 0]
        self.assertGreater(np.linalg.norm(m[0]-np.kron(local, np.eye(2))), .5)

    def test_optimal_readouts_attain_bounds_with_all_outcomes(self):
        self.assertEqual(len(self.rows), 35)
        for label, theta in B["ANGLES"]:
            for name, rho in E["probes"]().items():
                row = self.rows[label, name]
                c = abs(rho[0, 1])
                self.close(row["distances"]["initial_Q"], c*np.cos(theta))
                self.close(row["distances"]["initial_G"], c)
                self.close(row["distances"]["after_G_decode_Q"], c)
                for key, bound in (("optimal_Q", c*np.cos(theta)), ("optimal_G", c)):
                    m = row["readouts"][key]
                    self.close(m["quantum"], [.5+bound, .5-bound])
                    self.close(m["dephased"], [.5, .5])
                    self.close(m["total_variation"], bound)
                    for side in ("quantum", "dephased"):
                        self.assertEqual(len(m[side]), 2)
                        self.close(sum(m[side]), 1)
                        self.assertGreaterEqual(min(m[side]), -1e-10)
                for key in ("fixed_X", "fixed_Y"):
                    self.assertLessEqual(row["readouts"][key]["total_variation"],
                                         row["distances"]["initial_Q"]+1e-10)

    def test_blind_measurement_and_both_complex_phase_signs(self):
        row = self.rows["0", "plus_i"]
        self.close(row["readouts"]["fixed_X"]["quantum"], [.5, .5])
        self.close(row["readouts"]["fixed_Y"]["quantum"], [1, 0])
        self.close(row["readouts"]["optimal_Q"]["total_variation"], .5)
        self.close(self.rows["0", "minus_i"]["readouts"]["fixed_Y"]["quantum"], [0, 1])
        row = self.rows["pi/4", "plus_i"]
        self.close(row["readouts"]["fixed_X"]["quantum"], [.25, .75])
        self.close(row["readouts"]["optimal_Q"]["quantum"], [.5+1/(2*np.sqrt(2)),
                                                               .5-1/(2*np.sqrt(2))])
        # No rounding-away of a genuinely small coherence when choosing phase.
        self.close(E["optimal_phase"](1e-14j), -np.pi/2)
        self.close(E["optimal_phase"](0j), 0)

    def test_reaccess_counterexample_keeps_global_distance_constant(self):
        self.assertEqual(len(self.report["recoupling_controls"]), 2)
        for row in self.report["recoupling_controls"]:
            before = B["unpack"](row["initial_Q"])
            before_d = B["unpack"](row["initial_dephased_Q"])
            self.close(before, before_d)
            expected = np.zeros((8, 8), complex)
            expected[0, 0] = expected[6, 6] = .5
            self.close(before, expected)
            c = -.5j if row["input"] == "plus_i" else .5
            expected[0, 6], expected[6, 0] = c, np.conjugate(c)
            self.close(B["unpack"](row["after_E_inverse_Q"]), expected)
            self.close([row["initial_Q_distance"], row["after_E_inverse_Q_distance"],
                        row["initial_G_distance"], row["after_E_inverse_G_distance"]], [0, .5, .5, .5])
            self.close(row["subsequent_Q_readout"]["quantum"], [1, 0])
            self.close(row["subsequent_Q_readout"]["dephased"], [.5, .5])

    def test_r5b_reference_and_invalid_readouts(self):
        self.assertEqual(self.report["r5b_reference_checks"]["case_count"], 25)
        self.close(self.report["r5b_reference_checks"]["maximum_error"], 0)
        for phi in ([0], 1j, np.nan, np.inf):
            with self.assertRaises(ValueError):
                E["readout"](0., "Q", phi)
        with self.assertRaises(ValueError):
            E["decoder"](0., "invalid")

    def test_saved_evidence_and_source_hashes(self):
        self.assertTrue(self.report["summary"]["all_checks_within_tolerance"])
        saved = json.loads((ROOT / "results/r5c_access_guarantees.json").read_text())
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

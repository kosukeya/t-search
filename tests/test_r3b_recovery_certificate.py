"""Data-boundary, independent-channel and reference checks for r3a-v1."""
import hashlib
import itertools
import json
from pathlib import Path
import runpy
import unittest
from unittest.mock import patch
import numpy as np

ROOT = Path(__file__).resolve().parents[1]
E = runpy.run_path(str(ROOT/"experiments/r3b_recovery_certificate.py"))
F = E["CERT"]["certify"]


def unpack(data):
    out = np.zeros((data["dimension"], data["dimension"]), complex)
    for i, j, a, b in data["entries"]:
        out[i, j] = a+1j*b
    return out


def oracle(case, a):
    if case in ("no_record", "records_E_off"):
        return a
    if case == "records_E_on":
        return np.diag(np.diag(a))
    if case == "phase_flip":
        return a*np.array([[1, -1], [-1, 1]])
    if case == "replace_plus":
        return np.trace(a)*np.ones((2, 2))/2
    # Independent Pauli-transfer coefficients, including the imaginary/Y sector.
    lx, ly, lz = (.5, 0., .5) if case == "pauli_A" else (.5, 1., .5)
    t, z = np.trace(a), a[0, 0]-a[1, 1]
    x, y = a[0, 1]+a[1, 0], 1j*(a[0, 1]-a[1, 0])
    return np.array([[t+lz*z, lx*x-1j*ly*y], [lx*x+1j*ly*y, t-lz*z]])/2


class RecoveryCertificateTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.report = E["run_experiment"]()

    def close(self, a, b):
        np.testing.assert_allclose(a, b, atol=1e-10, rtol=0)

    def test_data_only_contract_and_orchestration(self):
        calls = []
        def spy(*, probabilities, assumptions):
            self.assertEqual(set(probabilities), {"z0", "z1", "x_plus", "x_minus"})
            self.assertTrue(all(isinstance(v, float) for v in probabilities.values()))
            self.assertEqual(assumptions, E["ASSUMPTIONS"])
            calls.append(dict(probabilities))
            return F(probabilities, assumptions)
        with patch.dict(E["run_experiment"].__globals__, {"certify": spy}):
            report = E["run_experiment"]()
        self.assertEqual(len(calls), 7)
        for row, data in zip(report["cases"], calls):
            self.assertEqual(row["certificate"], F(data, E["ASSUMPTIONS"]))
        with self.assertRaises(TypeError):
            F(calls[0], E["ASSUMPTIONS"], truth=1.)

    def test_reject_missing_false_assumptions_and_leaked_metadata(self):
        good = dict.fromkeys(E["CERT"]["PROBABILITY_KEYS"], .75)
        for key in E["ASSUMPTIONS"]:
            for bad in (False, None, 1):
                assumptions = dict(E["ASSUMPTIONS"], **{key: bad})
                with self.assertRaises(ValueError):
                    F(good, assumptions)
        with self.assertRaises(ValueError):
            F(good, {})
        for extra in ("case_id", "reference_fidelity", "Choi"):
            with self.assertRaises(ValueError):
                F(dict(good, **{extra: 1}), E["ASSUMPTIONS"])

    def test_invalid_probability_data_are_not_repaired(self):
        good = dict.fromkeys(E["CERT"]["PROBABILITY_KEYS"], .75)
        for invalid in (-1e-16, 1+1e-12, float("nan"), float("inf"), True, "0.75", 1j):
            with self.assertRaises(ValueError):
                F(dict(good, z0=invalid), E["ASSUMPTIONS"])
        with self.assertRaises(ValueError):
            F({"z0": 1}, E["ASSUMPTIONS"])

    def test_threshold_guard_never_licenses_a_boundary_claim(self):
        margin = E["CERT"]["NUMERICAL_MARGIN"]
        for delta, decision in ((0, False), (margin/2, False), (2*margin, True)):
            result = F({"z0": 1., "z1": 1., "x_plus": .5+delta, "x_minus": .5+delta}, E["ASSUMPTIONS"])
            self.assertEqual(result["non_measure_prepare_certified"], decision)
            self.close(result["lower_bound"], .5+delta)
        exact = F(dict.fromkeys(E["CERT"]["PROBABILITY_KEYS"], 1.), E["ASSUMPTIONS"])
        self.assertEqual((exact["lower_bound"], exact["upper_bound"]), (1., 1.))

    def test_all_channels_on_full_operator_basis_and_complex_probe(self):
        operators = []
        for i, j in itertools.product((0, 1), repeat=2):
            a = np.zeros((2, 2), complex); a[i, j] = 1
            operators.append(a)
        operators.append(np.array([[.5, -.5j], [.5j, .5]]))
        for case in E["CASE_IDS"]:
            for a in operators:
                self.close(E["C"]["apply_kraus"](a, E["channel"](case)), oracle(case, a))

    def test_both_measurement_outcomes_against_direct_states(self):
        v = {"z0": np.array([1, 0]), "z1": np.array([0, 1]),
             "x_plus": np.array([1, 1])/np.sqrt(2), "x_minus": np.array([1, -1])/np.sqrt(2)}
        for row in self.report["cases"]:
            for setting in row["measurements"]:
                psi = v[setting["input"]]
                expected = oracle(row["case_id"], np.outer(psi, psi))
                self.close(unpack(setting["output_state"]), expected)
                for i, name in enumerate(setting["outcome_labels"]):
                    self.close(setting["outcome_probabilities"][i], np.vdot(v[name], expected @ v[name]).real)
                self.close(np.sum(setting["kraus_branch_probabilities"], axis=0), setting["outcome_probabilities"])
                self.close(sum(setting["outcome_probabilities"]), 1.)

    def test_reference_truth_by_matrix_units_and_trace_formula(self):
        phi = np.array([1, 0, 0, 1])/np.sqrt(2)
        for row in self.report["cases"]:
            choi = np.zeros((4, 4), complex)
            for i, j in itertools.product((0, 1), repeat=2):
                a = np.zeros((2, 2), complex); a[i, j] = 1
                choi += np.kron(a, oracle(row["case_id"], a))/2
            truth = row["reference_truth"]
            self.close(unpack(truth["reference_output"]), choi)
            self.close(truth["entanglement_fidelity"], np.vdot(phi, choi @ phi).real)
            self.close(truth["entanglement_fidelity"], sum(abs(np.trace(k))**2 for k in E["channel"](row["case_id"]))/4)

    def test_expected_intervals_and_containment(self):
        expected = [(1,1,1,1,1), (1,1,1,1,1), (1,.5,.5,.5,.5),
                    (1,0,0,0,0), (.5,.5,0,.5,.25), (.75,.75,.5,.75,.5), (.75,.75,.5,.75,.75)]
        for row, values in zip(self.report["cases"], expected):
            c = row["certificate"]; fe = row["reference_truth"]["entanglement_fidelity"]
            self.close([c[k] for k in ("F_Z", "F_X", "lower_bound", "upper_bound")]+[fe], values)
            self.assertLessEqual(row["interval_violation"], 1e-10)
        self.assertEqual(self.report["summary"]["certified_case_count"], 2)

    def test_identical_two_basis_data_do_not_determine_fidelity(self):
        a, b = self.report["cases"][-2:]
        self.close(list(a["certificate_input"]["probabilities"].values()), list(b["certificate_input"]["probabilities"].values()))
        for k in ("F_Z", "F_X", "lower_bound", "upper_bound"):
            self.close(a["certificate"][k], b["certificate"][k])
        self.close(b["reference_truth"]["entanglement_fidelity"]-a["reference_truth"]["entanglement_fidelity"], .25)
        self.assertFalse(b["certificate"]["non_measure_prepare_certified"])

    def test_z_only_and_known_state_success_are_not_general_recovery(self):
        rows = {r["case_id"]: r for r in self.report["cases"]}
        self.close(rows["phase_flip"]["certificate"]["F_Z"], 1.)
        self.close(rows["phase_flip"]["reference_truth"]["entanglement_fidelity"], 0.)
        z = E["channel"]("phase_flip")[0]
        self.close(z @ z, np.eye(2))  # poor implemented identity fidelity is not irrecoverability
        replacement = rows["replace_plus"]
        self.close(replacement["certificate_input"]["probabilities"]["x_plus"], 1.)
        self.close(replacement["reference_truth"]["entanglement_fidelity"], .25)

    def test_cptp_full_space_and_physical_states(self):
        for row in self.report["cases"]:
            ops = E["channel"](row["case_id"])
            self.close(sum(k.conj().T @ k for k in ops), np.eye(2))
            truth = row["reference_truth"]
            self.close(truth["reference_marginal_residual_fro"], 0.)
            states = [unpack(truth["reference_output"])]+[unpack(s["output_state"]) for s in row["measurements"]]
            for rho in states:
                self.close(rho, rho.conj().T); self.close(np.trace(rho), 1.)
                self.assertGreaterEqual(np.linalg.eigvalsh(rho).min(), -1e-10)
        for condition in E["B"]["CONDITIONS"]:
            for fn in ("encoding_kraus", "decoder_kraus"):
                self.close(E["C"]["tp_residual"](E["C"][fn](condition, "Q")), 0.)

    def test_saved_result_and_source_hashes(self):
        saved = json.loads((ROOT/"results/r3b_recovery_certificate.json").read_text())
        self.assertEqual(saved["summary"]["case_count"], 7)
        self.assertEqual(saved["summary"]["setting_count"], 28)
        for path, digest in saved["provenance"]["source_sha256"].items():
            self.assertEqual(hashlib.sha256((ROOT/path).read_bytes()).hexdigest(), digest)
        def compare(a, b):
            if isinstance(a, dict):
                self.assertEqual(set(a), set(b))
                for k in a: compare(a[k], b[k])
            elif isinstance(a, list):
                self.assertEqual(len(a), len(b))
                for x, y in zip(a, b): compare(x, y)
            elif isinstance(a, bool): self.assertIs(a, b)
            elif isinstance(a, (int, float)): self.close(a, b)
            else: self.assertEqual(a, b)
        compare({k:v for k,v in saved.items() if k != "provenance"},
                {k:v for k,v in self.report.items() if k != "provenance"})


if __name__ == "__main__":
    unittest.main()

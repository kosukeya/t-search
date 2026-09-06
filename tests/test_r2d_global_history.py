"""Independent basis, spectral, probability and boundary checks for R2d."""
import hashlib
import itertools
import json
from pathlib import Path
import runpy
import unittest
import numpy as np

ROOT = Path(__file__).resolve().parents[1]
M = runpy.run_path(str(ROOT/"experiments/r2d_global_history.py"))
B = M["B"]
C = runpy.run_path(str(ROOT/"experiments/r2c_retention_recovery.py"))


def unpack(data):
    a = np.zeros((data["dimension"], data["dimension"]), complex)
    for i, j, real, imag in data["entries"]:
        a[i, j] = real+1j*imag
    return a


def image_index(condition, event, bit):
    # Direct bit strings for the ready-state basis; no production gates reused.
    written = condition != "no_record"
    return bit*(8 + (4 if written and event >= 1 else 0) +
                (2 if written and event >= 2 else 0) +
                (1 if condition == "records_E_on" and event == 3 else 0))


class GlobalHistoryTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.report = M["run_experiment"]()

    def close(self, a, b):
        np.testing.assert_allclose(a, b, atol=1e-10, rtol=0)

    def test_steps_on_all_basis_states(self):
        for condition in B["CONDITIONS"]:
            for k, u in enumerate(M["steps"](condition), 1):
                for col in range(16):
                    active = condition != "no_record" and (k < 3 or condition == "records_E_on")
                    row = col ^ (1 << (3-k)) if active and col & 8 else col
                    self.close(u[:, col], np.eye(16)[:, row])

    def test_history_channel_on_complete_input_operator_basis(self):
        for condition in B["CONDITIONS"]:
            jmap = M["construction"](condition)["J"]
            for a, b in itertools.product((0, 1), repeat=2):
                unit = np.zeros((2, 2), complex)
                unit[a, b] = 1
                expected = np.zeros((64, 64), complex)
                for j, k in itertools.product(range(4), repeat=2):
                    expected[16*j+image_index(condition, j, a),
                             16*k+image_index(condition, k, b)] = .25
                self.close(jmap @ unit @ jmap.conj().T, expected)
                for j in range(4):
                    out = np.zeros((16, 16), complex)
                    out[image_index(condition, j, a), image_index(condition, j, b)] = 1
                    self.close(M["conditioned_operator"](expected, j), out)

    def test_kernel_spectrum_and_ready_subspace(self):
        expected_spectrum = np.repeat([0, 1-1/np.sqrt(2), 1, 1+1/np.sqrt(2)], 16)
        for condition in B["CONDITIONS"]:
            m = M["construction"](condition)
            ep, vp = np.linalg.eigh(m["H_prop"])
            er, vr = np.linalg.eigh(m["H_ready"])
            self.close(ep, expected_spectrum)
            self.assertEqual(sum(abs(ep) < 1e-10), 16)
            self.assertEqual(sum(abs(er) < 1e-10), 2)
            self.assertGreaterEqual(er.min(), -1e-10)
            self.close(vp[:, :16] @ vp[:, :16].conj().T, m["W"] @ m["W"].conj().T)
            self.close(vr[:, :2] @ vr[:, :2].conj().T, m["J"] @ m["J"].conj().T)
            self.close(m["J"].conj().T @ m["J"], np.eye(2))

    def test_boundary_and_broken_propagation_controls(self):
        for condition in B["CONDITIONS"]:
            m = M["construction"](condition)
            wrong_ready = m["W"][:, 4]  # S=0, F1=1 initially
            self.close(m["H_prop"] @ wrong_ready, 0)
            self.close(np.vdot(wrong_ready, m["H_ready"] @ wrong_ready), .25)
            broken = m["J"][:, 0].copy()
            broken[16:32] *= -1  # preserves event probabilities; violates two edges
            self.assertGreater(np.linalg.norm(m["P"] @ broken), .5)
            self.close(m["H_ready"] @ m["J"], 0)

    def test_joint_instrument_completeness_and_independent_branches(self):
        for readout in B["READOUTS"]:
            all_k = [k for j in range(4) for _, k in M["joint_instrument_kraus"](j, readout)]
            self.close(sum(k.conj().T @ k for k in all_k), np.eye(64))
            for j in range(4):
                ks = M["joint_instrument_kraus"](j, readout)
                event_projector = np.zeros((64, 64))
                event_projector[16*j:16*(j+1), 16*j:16*(j+1)] = np.eye(16)
                self.close(sum(k.conj().T @ k for _, k in ks), event_projector)
                for condition in B["CONDITIONS"]:
                    rho = B["inputs"]()["asymmetric_mixed"]
                    omega = M["history_state"](rho, condition)
                    for outcome, k in ks:
                        expected = np.zeros((16, 16), complex)
                        for a, b in itertools.product((0, 1), repeat=2):
                            i, l = image_index(condition, j, a), image_index(condition, j, b)
                            if all(((i >> (3-t)) & 1) == o and ((l >> (3-t)) & 1) == o
                                   for t, o in zip(readout, outcome)):
                                expected[i, l] = rho[a, b]/4
                        self.close(k @ omega @ k.conj().T, expected)

    def test_calibration_timeline_from_deterministic_bit_records(self):
        for row in self.report["calibrations"]:
            expected = np.zeros((2, 2, 2))
            for b in (0, 1):
                index = image_index(row["condition"], row["event"], b)
                expected[b, (index >> 2) & 1, (index >> 1) & 1] = .5
            self.close(row["joint_probabilities_given_event"], expected)
            self.close(row["analytic_max_error"], 0)

    def test_event_states_disturbance_and_all_branch_diagnostics(self):
        for case in self.report["cases"]:
            self.close(case["history_constraint_residual_fro"], 0)
            for event in case["events"]:
                self.close(event["probability"], .25)
                self.close(event["conditional_vs_circuit_residual_fro"], 0)
                for row in event["readouts"]:
                    self.close(row["analytic_max_error"], 0)
                    self.close(sum(b["joint_probability_event_outcome"] for b in row["branches"]), .25)
                    self.close(sum(b["probability_given_event"] for b in row["branches"]), 1)
                    for branch in row["branches"]:
                        self.close(branch["conditional_branch_vs_circuit_residual_fro"], 0)
        plus = next(c for c in self.report["cases"] if c["condition"] == "records_E_on" and c["input"] == "plus")
        self.close([e["readouts"][2]["disturbance"]["Q"] for e in plus["events"]], [0, .5, .5, 0])
        self.close([e["readouts"][2]["disturbance"]["G"] for e in plus["events"]], [0, .5, .5, .5])

    def test_event_dephasing_control_keeps_slices_but_violates_constraint(self):
        for case in self.report["cases"]:
            omega = unpack(case["history_state"])
            classical = np.zeros_like(omega)
            for j in range(4):
                classical[16*j:16*(j+1), 16*j:16*(j+1)] = omega[16*j:16*(j+1), 16*j:16*(j+1)]
                self.close(M["conditioned_operator"](classical, j), M["conditioned_operator"](omega, j))
            h = M["construction"](case["condition"])["H_prop"]
            self.close(np.trace(h @ classical), .75)
            self.close(case["event_dephased_propagation_energy"], .75)

    def test_terminal_channel_transfers_r2c_reference_recovery(self):
        saved = json.loads((ROOT/"results/r2c_retention_recovery.json").read_text())
        for row in saved["recovery_cases"]:
            condition, scope = row["condition"], row["scope"]
            jmap = M["construction"](condition)["J"]
            choi = np.zeros((4, 4), complex)
            for a, b in itertools.product((0, 1), repeat=2):
                unit = np.zeros((2, 2), complex)
                unit[a, b] = 1
                terminal = M["conditioned_operator"](jmap @ unit @ jmap.conj().T, 3)
                self.close(terminal, B["encoding"](condition) @ unit @ B["encoding"](condition).conj().T)
                if scope == "Q":
                    terminal = np.trace(terminal.reshape(8, 2, 8, 2), axis1=1, axis2=3)
                output = C["apply_kraus"](terminal, C["decoder_kraus"](condition, scope))
                expected = np.diag(np.diag(unit)) if condition == "records_E_on" and scope == "Q" else unit
                self.close(output, expected)
                choi += np.kron(unit, output)/2
            self.close(choi, unpack(row["recovered_reference_state"]))
            self.close(np.trace(C["bell_state"]() @ choi), row["achieved_entanglement_fidelity"])

    def test_physical_validity_and_invalid_requests(self):
        for case in self.report["cases"]:
            for state in [unpack(case["history_state"])]+[unpack(e["conditional_state"]) for e in case["events"]]:
                self.close(state, state.conj().T)
                self.close(np.trace(state), 1)
                self.assertGreaterEqual(np.linalg.eigvalsh(state).min(), -1e-10)
        for action in (lambda: M["construction"]("unknown"),
                       lambda: M["event_block"](np.eye(64), 4),
                       lambda: M["history_state"](np.eye(2), "no_record")):
            with self.assertRaises(ValueError):
                action()

    def test_saved_results_and_source_hashes(self):
        saved = json.loads((ROOT/"results/r2d_global_history.json").read_text())
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

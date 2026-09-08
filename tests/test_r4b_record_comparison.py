"""Independent state/history oracles and the r4b-v1 negative controls."""
import hashlib
import itertools
import json
from pathlib import Path
import runpy
import unittest

import numpy as np

ROOT = Path(__file__).resolve().parents[1]
E = runpy.run_path(str(ROOT / "experiments/r4b_record_comparison.py"))


def unpack(data):
    matrix = np.zeros(data["shape"], complex)
    for i, j, real, imag in data["entries"]:
        matrix[i, j] = real + 1j*imag
    return matrix


def state_oracle(rho, context, environment, event):
    # Direct basis support from the protocol, independent of gate multiplication.
    one = [8, 12, 12+environment,
           (12 if context == "undo" else 14)+environment,
           {"read": 14, "undo": 8, "copy_undo": 10}[context]+environment][event]
    state = np.zeros((16, 16), complex)
    state[np.ix_([0, one], [0, one])] = rho
    return state


def history_oracle(rho, context, environment):
    # Trace out branch markers explicitly, rather than reconstructing chains.
    labels = list(itertools.product((0, 1), itertools.product((1, -1), (0, 1), (0, 1))))
    d = np.zeros((16, 16), complex)
    def markers(b):
        return {"read": (b, b), "undo": (0, 0), "copy_undo": (0, b)}[context]
    for i, (b, (s, f, g)) in enumerate(labels):
        for j, (c, other) in enumerate(labels):
            if (s, f, g) == other and (f, g) == markers(b) == markers(c) and environment*b == environment*c:
                d[i, j] = rho[b, c] * s**(b+c)/2
    return d


class RecordComparisonTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.report = E["run_experiment"]()
        cls.rows = {(r["context"], r["environment"], r["input"]): r for r in cls.report["cases"]}

    def close(self, a, b):
        np.testing.assert_allclose(a, b, atol=1e-10, rtol=0)

    def test_copy_gate_uses_friend_as_control_on_full_space(self):
        for control, target in ((0, 1), (1, 2), (1, 3)):
            u = E["cnot"](control, target)
            for col in range(16):
                bits = [int(x) for x in f"{col:04b}"]
                bits[target] = (bits[target]+bits[control]) % 2
                row = int("".join(map(str, bits)), 2)
                self.close(u[:, col], np.eye(16)[:, row])
            self.close(u.conj().T @ u, np.eye(16))
        # Off the initial code space, F1->F2 differs from the old S->F2 gate.
        self.assertFalse(np.allclose(E["cnot"](1, 2), E["cnot"](0, 2)))

    def test_scope_and_measurement_completeness(self):
        for context, env in itertools.product(E["CONTEXTS"], (0, 1)):
            m = E["model"](context, env)
            self.assertEqual(len(m["operations"]), 4)
            self.close(sum(m["terminal"]), np.eye(16))
            for p, q in itertools.product(range(8), repeat=2):
                self.close(m["terminal"][p] @ m["terminal"][q], m["terminal"][p] if p == q else np.zeros((16, 16)))
            # Continuation and readout are identity on E, including coherences.
            for op in m["operations"][2:] + list(m["terminal"]):
                q = op.reshape(8, 2, 8, 2)[:, 0, :, 0]
                self.close(op, np.kron(q, np.eye(2)))

    def test_all_event_states_and_full_input_operator_basis(self):
        for context, env in itertools.product(E["CONTEXTS"], (0, 1)):
            m = E["model"](context, env)
            for i, j in itertools.product((0, 1), repeat=2):
                a = np.zeros((2, 2), complex)
                a[i, j] = 1
                for event, v in enumerate(m["cumulative"]):
                    encoded = v @ m["embedding"]
                    self.close(encoded @ a @ encoded.conj().T, state_oracle(a, context, env, event))
        for row in self.report["cases"]:
            for event in row["events"]:
                expected = state_oracle(unpack(row["input_state"]), row["context"], row["environment"], event["event"])
                self.close(unpack(event["state_G"]), expected)
                # Independent trace over the last qubit.
                self.close(unpack(event["state_Q"]), expected.reshape(8, 2, 8, 2).trace(axis1=1, axis2=3))

    def test_all_terminal_probabilities_by_bra_projection(self):
        for row in self.report["cases"]:
            state = state_oracle(unpack(row["input_state"]), row["context"], row["environment"], 4)
            expected = []
            for sign, f, g in self.report["outcome_labels"]:
                total = 0.
                for env in (0, 1):
                    bra_ket = np.zeros(16, complex)
                    bra_ket[4*f+2*g+env] = 1/np.sqrt(2)
                    bra_ket[8+4*f+2*g+env] = sign/np.sqrt(2)
                    total += np.vdot(bra_ket, state @ bra_ket).real
                expected.append(total)
            self.close(row["terminal_probabilities"], expected)
            self.close(sum(expected), 1.)
            self.assertGreaterEqual(min(row["terminal_probabilities"]), -1e-10)

    def test_complete_complex_history_functional_and_coarse_graining(self):
        for row in self.report["cases"]:
            h = row["history"]
            d = unpack(h["decoherence_functional"])
            expected = history_oracle(unpack(row["input_state"]), row["context"], row["environment"])
            self.close(d, expected)
            self.close(d, d.conj().T)
            self.assertGreaterEqual(np.linalg.eigvalsh(d).min(), -1e-10)
            self.close(np.trace(d), 1.)
            self.close(h["coarse_probabilities"], row["terminal_probabilities"])
            self.close(h["diagonal_sum_probabilities"], h["inserted_measurement_probabilities"])

    def test_intermediate_measurement_is_a_distinct_circuit(self):
        row = self.rows["undo", 0, "plus"]
        self.close(row["x_plus_probability"], 1.)
        self.close(row["history"]["inserted_measurement_probabilities"][0], .5)
        self.close(row["history"]["actual_vs_inserted_total_variation"], .5)
        d = unpack(row["history"]["decoherence_functional"])
        self.close(d[0, 8], .25)
        self.close(d[4, 12], -.25)
        self.assertFalse(row["history"]["weakly_consistent"])
        for context, env in (("read", 0), ("read", 1), ("undo", 1), ("copy_undo", 0), ("copy_undo", 1)):
            h = self.rows[context, env, "plus"]["history"]
            self.close(h["max_offdiagonal_abs"], 0.)
            self.assertTrue(h["medium_decoherent"])

    def test_imaginary_cross_terms_are_not_probability_disagreement(self):
        row = self.rows["undo", 0, "plus_i"]
        h = row["history"]
        d = unpack(h["decoherence_functional"])
        self.close(d[0, 8], -.25j)
        self.close(d[4, 12], .25j)
        self.close(h["max_offdiagonal_abs"], .25)
        self.close(h["max_offdiagonal_real_abs"], 0.)
        self.close(h["actual_vs_inserted_total_variation"], 0.)
        self.close(row["terminal_probabilities"], h["inserted_measurement_probabilities"])
        self.assertFalse(h["medium_decoherent"])
        self.assertTrue(h["weakly_consistent"])

    def test_agreement_is_not_calibrated_record_accuracy(self):
        for row in self.report["calibration_summary"]:
            expected = {"read": (1., 1., 1.), "undo": (.5, .5, 1.), "copy_undo": (.5, 1., .5)}[row["context"]]
            self.close([row[k] for k in ("F1_correct", "F2_correct", "record_agreement")], expected)
        for name in ("plus", "plus_i"):
            for context, env in itertools.product(E["CONTEXTS"], (0, 1)):
                self.assertIsNone(self.rows[context, env, name]["calibration"])
        # No stale friend value is carried through the undo.
        row = self.rows["undo", 0, "one"]
        self.close(row["events"][2]["z_record_probabilities"], [0, 0, 1, 0])
        self.close(row["events"][4]["z_record_probabilities"], [1, 0, 0, 0])

    def test_s_interference_and_q_coherence_are_distinct(self):
        off = self.rows["copy_undo", 0, "plus"]
        on = self.rows["copy_undo", 1, "plus"]
        self.close(off["x_plus_probability"], .5)
        self.close(on["x_plus_probability"], .5)
        self.close(unpack(off["events"][4]["state_Q"])[0, 5], .5)
        self.close(unpack(on["events"][4]["state_Q"])[0, 5], 0.)

    def test_five_event_history_on_operator_basis(self):
        for context, env in itertools.product(E["CONTEXTS"], (0, 1)):
            m = E["model"](context, env)
            jmap = m["J"]
            self.close(jmap.conj().T @ jmap, np.eye(2))
            for i, j in itertools.product((0, 1), repeat=2):
                a = np.zeros((2, 2), complex)
                a[i, j] = 1
                history = jmap @ a @ jmap.conj().T
                for event in range(5):
                    self.close(5*history[16*event:16*(event+1), 16*event:16*(event+1)], state_oracle(a, context, env, event))
        for row in self.report["cases"]:
            self.close(list(row["global_history"].values()), [0, 0, 0])
            for event in row["events"]:
                self.close(event["history_weight"], .2)
                self.close(event["history_reconstruction_residual_fro"], 0.)

    def test_summary_and_saved_evidence(self):
        summary = self.report["summary"]
        self.assertEqual((summary["case_count"], summary["outcomes_per_case"], summary["histories_per_case"]), (24, 8, 16))
        self.assertEqual((summary["medium_decoherent_count"], summary["weakly_consistent_count"]), (22, 23))
        self.assertTrue(summary["all_checks_within_tolerance"])
        saved = json.loads((ROOT / "results/r4b_record_comparison.json").read_text())
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

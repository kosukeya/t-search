"""r5b-v1: fixed pointer dephasing versus quantum partial records.

Single-copy state-pair distances; all outcomes retained. No shots, clipping,
postselection, environment reset, or R5c optimal-measurement implementation.
"""
from __future__ import annotations

import hashlib
import itertools
import json
from pathlib import Path
import platform
import runpy

import numpy as np

ROOT = Path(__file__).resolve().parents[1]
R4 = runpy.run_path(str(ROOT / "experiments/r4b_record_comparison.py"))
B = R4["B"]
ATOL = 1e-10
BASELINE = "1d751d2f3309e9014b8d4904104d2bfa866024e0"
MAIN_MERGE = "baed792419537c08d9bdc0990ed8b345549f6d98"
ANGLES = (("0", 0.), ("pi/6", np.pi/6), ("pi/4", np.pi/4),
          ("pi/3", np.pi/3), ("pi/2", np.pi/2))
SOURCE_PATHS = ("experiments/r5b_record_stability.py",
                "tests/test_r5b_record_stability.py",
                "experiments/r4b_record_comparison.py",
                "experiments/r2_shared_records.py",
                "docs/t_search_r5_protocol.md",
                "docs/t_search_r5a_definition_audit.md")
REFERENCE_PATH = "results/r4b_record_comparison.json"
packed = R4["packed"]
tensor = R4["tensor"]
cnot = R4["cnot"]
probs = R4["probabilities"]
marginal = B["marginal"]
distance = B["distance"]


def unpack(data):
    out = np.zeros(data["shape"], complex)
    for i, j, real, imag in data["entries"]:
        out[i, j] = real + 1j*imag
    return out


def probes():
    return {**R4["probes"](), "maximally_mixed": np.eye(2)/2}


def environment_gate(theta):
    if not np.isscalar(theta) or not np.isreal(theta):
        raise ValueError("theta must be a real scalar")
    theta = float(np.real(theta))
    if not np.isfinite(theta) or not 0 <= theta <= np.pi/2:
        raise ValueError("theta must be in [0, pi/2]")
    ident = np.eye(2)
    x = np.array([[0, 1], [1, 0]])
    v = np.exp(1j*theta)*(np.cos(theta)*ident-1j*np.sin(theta)*x)
    return (tensor(ident, np.diag([1, 0]), ident, ident)
            + tensor(ident, np.diag([0, 1]), ident, v))


def embedding(theta):
    return (environment_gate(theta) @ cnot(0, 1))[:, [0, 8]]


def oracle_embedding(theta):
    """Independent spectral expression: conditional E amplitudes at 12,13."""
    phase = np.exp(2j*theta)
    w = np.zeros((16, 2), complex)
    w[0, 0] = 1
    w[12, 1], w[13, 1] = (1+phase)/2, (1-phase)/2
    return w


def pointer_projectors():
    return [tensor(np.eye(2), np.diag([b == 0, b == 1]), np.eye(2), np.eye(2))
            for b in (0, 1)]


def dephase(state):
    return sum((p @ state @ p for p in pointer_projectors()), np.zeros_like(state))


def pointer_measurement():
    return np.array([tensor(np.eye(2), np.diag([f == 0, f == 1]),
                            np.diag([g == 0, g == 1]), np.eye(2))
                     for f, g in itertools.product((0, 1), repeat=2)])


def undo_x_measurement():
    undo = cnot(0, 1)
    return np.array([undo.conj().T @ tensor(np.array([[1, s], [s, 1]])/2,
                                           np.eye(2), np.eye(2), np.eye(2)) @ undo
                     for s in (1, -1)])


def measurement_pair(measurement, state, dephased):
    a, b = probs(measurement, state), probs(measurement, dephased)
    return {"quantum": a.tolist(), "dephased": b.tolist(),
            "total_variation": float(np.abs(a-b).sum()/2),
            "normalization_error": float(max(abs(a.sum()-1), abs(b.sum()-1))),
            "minimum_probability": float(min(a.min(), b.min())),
            "max_imaginary_probability": float(max(
                np.abs(np.einsum("oij,ji->o", measurement, state).imag).max(),
                np.abs(np.einsum("oij,ji->o", measurement, dephased).imag).max()))}


def analytic_states(theta, rho):
    w = oracle_embedding(theta)
    g, gd = w @ rho @ w.conj().T, w @ np.diag(np.diag(rho)) @ w.conj().T
    gamma = np.exp(1j*theta)*np.cos(theta)
    q, qd = np.zeros((8, 8), complex), np.zeros((8, 8), complex)
    q[0, 0], q[6, 6] = rho[0, 0], rho[1, 1]
    q[0, 6], q[6, 0] = rho[0, 1]*gamma.conjugate(), rho[1, 0]*gamma
    qd[0, 0], qd[6, 6] = rho[0, 0], rho[1, 1]
    return {"rho_G": g, "dephased_G": gd, "rho_Q": q, "dephased_Q": qd}


def case(angle_label, theta, name, rho):
    rho = B["validate_state"](rho, 2)
    w = embedding(theta)
    g = w @ rho @ w.conj().T
    gd = dephase(g)
    states = {"rho_G": g, "dephased_G": gd,
              "rho_Q": marginal(g, (0, 1, 2)), "dephased_Q": marginal(gd, (0, 1, 2))}
    oracle = analytic_states(theta, rho)
    zread = measurement_pair(pointer_measurement(), g, gd)
    xread = measurement_pair(undo_x_measurement(), g, gd)
    # Independently extract the overlap from the implemented conditional E state.
    gamma = w[12, 1]
    c = rho[0, 1]
    z = c*np.conjugate(gamma)
    expected_z = [float(rho[0, 0].real), 0., float(rho[1, 1].real), 0.]
    expected = {"C_Z": 0., "C_Q": float(abs(c)*np.cos(theta)), "C_G": float(abs(c)),
                "pointer_probabilities": expected_z,
                "undo_x_quantum": [.5+float(z.real), .5-float(z.real)],
                "undo_x_dephased": [.5, .5], "undo_x_signed_plus_difference": float(z.real)}
    observed = {"C_Z": zread["total_variation"],
                "C_Q": distance(states["rho_Q"], states["dephased_Q"]),
                "C_G": distance(g, gd)}
    state_errors = {k: float(np.max(np.abs(states[k]-oracle[k]))) for k in states}
    errors = list(state_errors.values()) + [abs(observed[k]-expected[k]) for k in observed]
    errors += [float(abs(gamma-np.exp(1j*theta)*np.cos(theta))),
               float(np.max(np.abs(np.array(zread["quantum"])-expected_z))),
               float(np.max(np.abs(np.array(zread["dephased"])-expected_z))),
               float(np.max(np.abs(np.array(xread["quantum"])-expected["undo_x_quantum"]))),
               float(np.max(np.abs(np.array(xread["dephased"])-expected["undo_x_dephased"])))]
    b = {"zero": 0, "one": 1}.get(name)
    calibration = None if b is None else {
        "prepared_z_value": b,
        "F1_correct": float(sum(zread["quantum"][2*f+g] for f, g in
                                itertools.product((0, 1), repeat=2) if f == b)),
        "F2_correct": float(sum(zread["quantum"][2*f+g] for f, g in
                                itertools.product((0, 1), repeat=2) if g == b))}
    return {"angle": angle_label, "theta": float(theta), "input": name,
            "input_state": packed(rho), "gamma": [float(gamma.real), float(gamma.imag)],
            "states": {k: packed(v) for k, v in states.items()},
            "state_diagnostics": {k: B["state_diagnostics"](v) for k, v in states.items()},
            "state_oracle_max_errors": state_errors, "distances": observed,
            "pointer_readout": zread, "undo_x_readout": xread, "calibration": calibration,
            "analytic": expected, "analytic_max_error": float(max(errors))}


def endpoint_checks(reference):
    checks = []
    for old in reference["cases"]:
        env, context, name = old["environment"], old["context"], old["input"]
        theta = env*np.pi/2
        rho = probes()[name]
        w = embedding(theta)
        state = w @ rho @ w.conj().T
        m = R4["model"](context, env)
        suffix = m["continuation"]
        final = suffix @ state @ suffix.conj().T
        terminal = probs(m["terminal"], final)
        residuals = {
            "environment_gate_max_error": float(np.max(np.abs(environment_gate(theta)-m["operations"][1]))),
            "event2_state_max_error": float(np.max(np.abs(state-unpack(old["events"][2]["state_G"])))),
            "terminal_state_max_error": float(np.max(np.abs(final-unpack(old["events"][4]["state_G"])))),
            "terminal_probabilities_max_error": float(np.max(np.abs(terminal-old["terminal_probabilities"])))}
        checks.append({"context": context, "environment": env, "input": name,
                       "event2_state_G": packed(state), "terminal_probabilities": terminal.tolist(),
                       "reference_terminal_probabilities": old["terminal_probabilities"],
                       "residuals": residuals})
    return checks


def no_record_controls():
    rows = []
    ready = np.zeros((8, 8), complex)
    ready[0, 0] = 1
    for name in ("zero", "one"):
        g = np.kron(probes()[name], ready)
        gd = dephase(g)
        r = measurement_pair(pointer_measurement(), g, gd)
        b = 0 if name == "zero" else 1
        rows.append({"input": name, "state_G": packed(g), "dephased_G": packed(gd),
                     "pointer_readout": r, "F1_correct": float(sum(
                         r["quantum"][2*f+h] for f, h in itertools.product((0, 1), repeat=2) if f == b)),
                     "distances": {"C_Z": r["total_variation"],
                                   "C_Q": distance(marginal(g, (0, 1, 2)), marginal(gd, (0, 1, 2))),
                                   "C_G": distance(g, gd)}})
    return {"definition": "rho_S tensor |000><000|; no record interaction",
            "cases": rows, "equal_z_input_weights": [.5, .5],
            "F1_correct": sum(x["F1_correct"] for x in rows)/2}


def run_experiment():
    reference = json.loads((ROOT / REFERENCE_PATH).read_text())
    rows = [case(label, theta, name, rho) for label, theta in ANGLES
            for name, rho in probes().items()]
    endpoints, no_record = endpoint_checks(reference), no_record_controls()
    gates = [{"angle": label, "unitarity_residual_fro": float(np.linalg.norm(
                  environment_gate(t).conj().T @ environment_gate(t)-np.eye(16))),
              "isometry_residual_fro": float(np.linalg.norm(embedding(t).conj().T @ embedding(t)-np.eye(2))),
              "oracle_embedding_max_error": float(np.max(np.abs(embedding(t)-oracle_embedding(t))))}
             for label, t in ANGLES]
    calibrations = [{"angle": label, "equal_z_input_weights": [.5, .5],
                     "F1_correct": sum(r["calibration"]["F1_correct"] for r in rows
                                       if r["angle"] == label and r["calibration"] is not None)/2,
                     "F2_correct": sum(r["calibration"]["F2_correct"] for r in rows
                                       if r["angle"] == label and r["calibration"] is not None)/2}
                    for label, _ in ANGLES]
    completeness = float(np.linalg.norm(sum(p.conj().T @ p for p in pointer_projectors())-np.eye(16)))
    residuals = [completeness, abs(no_record["F1_correct"]-.5)]
    for gate in gates:
        residuals.extend(v for k, v in gate.items() if k != "angle")
    for row in rows:
        residuals.append(row["analytic_max_error"])
        for sd in row["state_diagnostics"].values():
            residuals.extend([sd["trace_error"], sd["hermitian_residual_fro"], max(0., -sd["minimum_eigenvalue"])])
        for m in (row["pointer_readout"], row["undo_x_readout"]):
            residuals.extend([m["normalization_error"], max(0., -m["minimum_probability"]), m["max_imaginary_probability"]])
        residuals.append(max(0., row["undo_x_readout"]["total_variation"]-row["distances"]["C_Q"]))
    for row in endpoints:
        residuals.extend(row["residuals"].values())
    for row in no_record["cases"]:
        residuals.extend(row["distances"].values())
    for row in calibrations:
        residuals.extend([abs(row["F1_correct"]-1), abs(row["F2_correct"]-.5)])
    checks_ok = bool(np.isfinite(residuals).all() and max(residuals) <= ATOL)
    return {"specification": "r5b-v1", "protocol": "r5-v1", "absolute_tolerance": ATOL,
            "relative_tolerance": 0, "provenance": {"baseline_commit": BASELINE,
                "r4_merge_commit": MAIN_MERGE, "python": platform.python_version(), "numpy": np.__version__,
                "source_sha256": {p: hashlib.sha256((ROOT/p).read_bytes()).hexdigest() for p in SOURCE_PATHS},
                "reference_sha256": {REFERENCE_PATH: hashlib.sha256((ROOT/REFERENCE_PATH).read_bytes()).hexdigest()}},
            "qubit_order": ["S", "F1", "F2", "E"], "checkpoint_event": 2,
            "pointer_outcomes": [[f, g] for f, g in itertools.product((0, 1), repeat=2)],
            "undo_x_outcomes": [1, -1], "endpoint_terminal_outcomes": [list(x) for x in R4["OUTCOMES"]],
            "access": {"C_Z": "F1/F2 Z readout and classical postprocessing only",
                       "C_Q": "all POVMs on Q=SF1F2; no subsequent E interaction or reset",
                       "C_G": "all POVMs on G=QE; explicit environment-access resource control"},
            "probability_semantics": "Born probabilities; all outcomes; no clipping, shots, or postselection",
            "distance_semantics": "single-copy TV supremum = trace distance for Q/G; analytic justification in R5a",
            "cases": rows, "calibration_summary": calibrations, "gate_diagnostics": gates,
            "dephasing_completeness_residual_fro": completeness, "endpoint_checks": endpoints,
            "no_record_control": no_record,
            "summary": {"case_count": len(rows), "endpoint_count": len(endpoints),
                        "no_record_case_count": len(no_record["cases"]),
                        "maximum_analytic_error": max(r["analytic_max_error"] for r in rows),
                        "maximum_endpoint_error": max(v for r in endpoints for v in r["residuals"].values()),
                        "maximum_verification_residual": float(max(residuals)),
                        "all_checks_within_tolerance": checks_ok},
            "limits": ["fixed pointer basis and dephasing counterfactual; not all classical models",
                       "continuous-class conclusion is analytic, not inferred from five sample angles",
                       "no optimal measurement circuit implemented (R5c pending)",
                       "not a certificate of good records, absolute facts, CPL, or ontological becoming",
                       "no reference-assisted channel discrimination or finite-shot confidence guarantee"]}


if __name__ == "__main__":
    result = run_experiment()
    if not result["summary"]["all_checks_within_tolerance"]:
        raise SystemExit("R5b verification failed; refusing to save results")
    output = ROOT / "results/r5b_record_stability.json"
    output.write_text(json.dumps(result, ensure_ascii=False, indent=2, allow_nan=False)+"\n")
    print(json.dumps(result["summary"], indent=2))

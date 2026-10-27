"""r5c-v1: constructive optimal readouts and an environment-recoupling control.

All-result Born distributions for known single-copy state pairs. The proof of
the all-POVM bound is analytic; the finite cases check its circuit realization.
"""
from __future__ import annotations

import hashlib
import json
from pathlib import Path
import platform
import runpy

import numpy as np

ROOT = Path(__file__).resolve().parents[1]
B = runpy.run_path(str(ROOT / "experiments/r5b_record_stability.py"))
ATOL = 1e-10
BASELINE = "a9c0849af737ca120833cb09eac369ef2de60fc4"
SOURCE_PATHS = ("experiments/r5c_access_guarantees.py",
                "tests/test_r5c_access_guarantees.py",
                "docs/t_search_r5c_protocol.md",
                "experiments/r5b_record_stability.py",
                "experiments/r4b_record_comparison.py",
                "experiments/r2_shared_records.py",
                "docs/t_search_r5_protocol.md",
                "docs/t_search_r5a_definition_audit.md")
REFERENCE_PATH = "results/r5b_record_stability.json"
I2 = np.eye(2, dtype=complex)
I16 = np.eye(16, dtype=complex)
H = np.array([[1, 1], [1, -1]], complex)/np.sqrt(2)
S_Z = B["tensor"](np.diag([1, 0]), I2, I2, I2)


def probes():
    minus_i = np.array([1, -1j])/np.sqrt(2)
    return {**B["probes"](), "minus_i": np.outer(minus_i, minus_i.conj()),
            "asymmetric_mixed": B["B"]["inputs"]()["asymmetric_mixed"]}


def optimal_phase(coherence):
    # Zero is handled exactly, without discarding small nonzero differences.
    return 0. if coherence == 0 else float(-np.angle(coherence))


def decoder(theta, scope):
    undo = B["cnot"](0, 1)
    if scope == "Q":
        return undo
    if scope == "G":
        return undo @ B["environment_gate"](theta).conj().T
    raise ValueError("scope must be Q or G")


def readout(theta, scope, phi):
    if not np.isscalar(phi) or not np.isreal(phi) or not np.isfinite(phi):
        raise ValueError("phi must be a finite real scalar")
    # Temporal order: decode, diag(1,exp(-i phi)), H, then Z on S.
    rotate = B["tensor"](H @ np.diag([1, np.exp(-1j*phi)]), I2, I2, I2)
    circuit = rotate @ decoder(theta, scope)
    plus = circuit.conj().T @ S_Z @ circuit
    return np.array([plus, I16-plus]), circuit


def povm_diagnostics(measurement):
    return {"completeness_residual_fro": float(np.linalg.norm(sum(measurement)-I16)),
            "hermitian_residual_fro": float(max(np.linalg.norm(m-m.conj().T) for m in measurement)),
            "projector_residual_fro": float(max(np.linalg.norm(m @ m-m) for m in measurement)),
            "minimum_eigenvalue": float(min(np.linalg.eigvalsh(m).min() for m in measurement))}


def case(label, theta, name, rho):
    rho = B["B"]["validate_state"](rho, 2)
    w = B["embedding"](theta)
    g = w @ rho @ w.conj().T
    gd = B["dephase"](g)
    q, qd = B["marginal"](g, (0, 1, 2)), B["marginal"](gd, (0, 1, 2))
    c, gamma = rho[0, 1], np.exp(1j*theta)*np.cos(theta)
    z = c*gamma.conjugate()
    definitions = {"fixed_X": ("Q", 0.), "fixed_Y": ("Q", np.pi/2),
                   "optimal_Q": ("Q", optimal_phase(z)),
                   "optimal_G": ("G", optimal_phase(c))}
    readouts, diagnostics, phases, circuits = {}, {}, {}, {}
    residuals = []
    for key, (scope, phi) in definitions.items():
        measurement, circuit = readout(theta, scope, phi)
        observed = B["measurement_pair"](measurement, g, gd)
        value = z if scope == "Q" else c
        signed = float(np.real(value*np.exp(1j*phi)))
        observed["expected_signed_plus_difference"] = signed
        observed["expected_quantum"] = [.5+signed, .5-signed]
        observed["expected_dephased"] = [.5, .5]
        observed["signed_plus_difference"] = observed["quantum"][0]-observed["dephased"][0]
        residuals.extend([abs(observed["total_variation"]-abs(signed)),
                          float(np.max(np.abs(np.array(observed["quantum"])-observed["expected_quantum"]))),
                          float(np.max(np.abs(np.array(observed["dephased"])-[.5, .5])))])
        d = povm_diagnostics(measurement)
        d["circuit_unitarity_residual_fro"] = float(np.linalg.norm(circuit.conj().T @ circuit-I16))
        if scope == "Q":
            local = circuit.reshape(8, 2, 8, 2)[:, 0, :, 0]
            d["Q_tensor_identity_E_residual_fro"] = float(np.linalg.norm(circuit-np.kron(local, I2)))
        readouts[key], diagnostics[key], phases[key], circuits[key] = observed, d, phi, circuit
    readouts["pointer_Z"] = B["measurement_pair"](B["pointer_measurement"](), g, gd)
    dq, dg = B["distance"](q, qd), B["distance"](g, gd)
    decode_g = decoder(theta, "G")
    after = decode_g @ g @ decode_g.conj().T
    after_d = decode_g @ gd @ decode_g.conj().T
    after_q, after_qd = B["marginal"](after, (0, 1, 2)), B["marginal"](after_d, (0, 1, 2))
    after_distance = B["distance"](after_q, after_qd)
    residuals.extend([abs(dq-abs(z)), abs(dg-abs(c)), abs(after_distance-abs(c)),
                      abs(readouts["optimal_Q"]["total_variation"]-dq),
                      abs(readouts["optimal_G"]["total_variation"]-dg),
                      readouts["pointer_Z"]["total_variation"]])
    for key in ("fixed_X", "fixed_Y"):
        residuals.append(max(0., readouts[key]["total_variation"]-dq))
    return {"angle": label, "theta": float(theta), "input": name,
            "input_state": B["packed"](rho), "gamma": [float(gamma.real), float(gamma.imag)],
            "z": [float(z.real), float(z.imag)], "phases": phases,
            "distances": {"initial_Q": dq, "initial_G": dg, "after_G_decode_Q": after_distance},
            "readouts": readouts, "measurement_diagnostics": diagnostics,
            "maximum_analytic_error": float(max(residuals))}


def recoupling_control(name):
    theta = np.pi/2
    rho = probes()[name]
    w = B["embedding"](theta)
    g, gd = w @ rho @ w.conj().T, B["dephase"](w @ rho @ w.conj().T)
    undo_e = B["environment_gate"](theta).conj().T
    after, after_d = undo_e @ g @ undo_e.conj().T, undo_e @ gd @ undo_e.conj().T
    initial_q, initial_qd = B["marginal"](g, (0, 1, 2)), B["marginal"](gd, (0, 1, 2))
    after_q, after_qd = B["marginal"](after, (0, 1, 2)), B["marginal"](after_d, (0, 1, 2))
    q_measurement, _ = readout(0., "Q", optimal_phase(rho[0, 1]))
    return {"input": name, "theta": float(theta),
            "initial_Q": B["packed"](initial_q), "initial_dephased_Q": B["packed"](initial_qd),
            "after_E_inverse_Q": B["packed"](after_q),
            "after_E_inverse_dephased_Q": B["packed"](after_qd),
            "initial_Q_distance": B["distance"](initial_q, initial_qd),
            "after_E_inverse_Q_distance": B["distance"](after_q, after_qd),
            "initial_G_distance": B["distance"](g, gd),
            "after_E_inverse_G_distance": B["distance"](after, after_d),
            "subsequent_Q_readout": B["measurement_pair"](q_measurement, after, after_d),
            "resources": "U_theta^dagger on F1E; then Q decoder and phase readout; no reset"}


def reference_checks(rows):
    reference = json.loads((ROOT / REFERENCE_PATH).read_text())
    lookup = {(r["angle"], r["input"]): r for r in rows}
    errors = []
    for old in reference["cases"]:
        new = lookup[old["angle"], old["input"]]
        errors.extend([abs(new["distances"]["initial_Q"]-old["distances"]["C_Q"]),
                       abs(new["distances"]["initial_G"]-old["distances"]["C_G"])])
        for side in ("quantum", "dephased"):
            errors.append(float(np.max(np.abs(np.array(new["readouts"]["fixed_X"][side])
                                            -old["undo_x_readout"][side]))))
            errors.append(float(np.max(np.abs(np.array(new["readouts"]["pointer_Z"][side])
                                            -old["pointer_readout"][side]))))
    return {"case_count": len(reference["cases"]), "maximum_error": max(errors)}


def run_experiment():
    rows = [case(label, theta, name, rho) for label, theta in B["ANGLES"]
            for name, rho in probes().items()]
    controls = [recoupling_control(name) for name in ("plus", "plus_i")]
    reference = reference_checks(rows)
    residuals = [reference["maximum_error"]]+[r["maximum_analytic_error"] for r in rows]
    for r in rows:
        for d in r["measurement_diagnostics"].values():
            residuals.extend(max(0., -v) if k == "minimum_eigenvalue" else v for k, v in d.items())
        for m in r["readouts"].values():
            residuals.extend([m["normalization_error"], max(0., -m["minimum_probability"]),
                              m["max_imaginary_probability"]])
    for r in controls:
        residuals.extend([r["initial_Q_distance"], abs(r["after_E_inverse_Q_distance"]-.5),
                          abs(r["initial_G_distance"]-.5), abs(r["after_E_inverse_G_distance"]-.5),
                          abs(r["subsequent_Q_readout"]["total_variation"]-.5)])
    maximum = float(max(residuals))
    return {"specification": "r5c-v1", "absolute_tolerance": ATOL, "relative_tolerance": 0,
            "provenance": {"baseline_commit": BASELINE, "python": platform.python_version(),
                "numpy": np.__version__,
                "source_sha256": {p: hashlib.sha256((ROOT/p).read_bytes()).hexdigest() for p in SOURCE_PATHS},
                "reference_sha256": {REFERENCE_PATH: hashlib.sha256((ROOT/REFERENCE_PATH).read_bytes()).hexdigest()}},
            "qubit_order": ["S", "F1", "F2", "E"], "checkpoint_event": 2,
            "readout_outcomes": ["S_Z=0 after declared circuit", "S_Z=1 after declared circuit"],
            "phase_convention": "m_phi=(|0>+exp(i phi)|1>)/sqrt(2); signed gap Re(z exp(i phi))",
            "measurement_design": "known state-pair phase; zero coherence uses phi=0; no threshold clipping",
            "probability_semantics": "all-result Born probabilities, no shots, clipping, reset or postselection",
            "cases": rows, "recoupling_controls": controls, "r5b_reference_checks": reference,
            "summary": {"case_count": len(rows), "recoupling_control_count": len(controls),
                        "maximum_analytic_error": max(r["maximum_analytic_error"] for r in rows),
                        "maximum_verification_residual": maximum,
                        "all_checks_within_tolerance": bool(np.isfinite(residuals).all() and maximum <= ATOL)},
            "limits": ["finite cases check analytic bounds, not an optimization over all circuits",
                       "optimal phase can depend on the known state pair, not a universal unknown-input measurement",
                       "Q guarantee assumes no subsequent E coupling; G decoder is a different resource",
                       "decoding erases records, not a nondemolition test preserving the original memory",
                       "not a certificate of actualization, absolute facts, CPL or ontological becoming"]}


if __name__ == "__main__":
    result = run_experiment()
    if not result["summary"]["all_checks_within_tolerance"]:
        raise SystemExit("R5c verification failed; refusing to save results")
    (ROOT / "results/r5c_access_guarantees.json").write_text(
        json.dumps(result, ensure_ascii=False, indent=2, allow_nan=False)+"\n")
    print(json.dumps(result["summary"], indent=2))

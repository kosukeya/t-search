from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PROTOCOL = (ROOT / "docs" / "stage15_protocol.md").read_text(encoding="utf-8")
FREEZE = (ROOT / "results" / "stage15_0_protocol_freeze.md").read_text(encoding="utf-8")
NOTES = (ROOT / "docs" / "stage15a_notes.md").read_text(encoding="utf-8")
RESULT = (ROOT / "results" / "stage15a_local_smeared.md").read_text(encoding="utf-8")

SOURCE_HEAD = "e53dadffbf94257ef15d37b2a817cfa4caa05913"


def test_stage15a_documents_preserve_the_frozen_carrier():
    combined = "\n".join((PROTOCOL, FREEZE, NOTES, RESULT))
    for phrase in (
        "K_i=pi_i+c_iP",
        "C_0=K_0+0.5 T_0 K_1",
        "C_1=K_1+0.5 T_1 K_2",
        "C_2=K_2",
        "{C_0,C_1}=-0.25 T_0 C_2",
        "108",
        "27",
        "-0.25, 0.0, 0.25",
    ):
        assert phrase in combined


def test_stage15a_source_checkpoint_and_diagnostics_are_recorded():
    combined = NOTES + "\n" + RESULT
    assert SOURCE_HEAD in combined
    for phrase in (
        "72 / 108",
        "1296",
        "0.685372710841757",
        "6.938893903907228e-18",
        "maximum unsmeared closure residual: **0.0**",
        "maximum Jacobi residual: **0.0**",
        "maximum smeared antisymmetry residual: **0.0**",
    ):
        assert phrase in combined


def test_stage15a_closes_only_criteria_11_through_17():
    combined = NOTES + "\n" + RESULT
    assert "criteria **11–17**" in combined
    assert "Criteria **18–50 remain pending**" in combined
    assert (
        "Stage 15A spatially indexed local/smeared first-class carrier and finite representative family = established"
        in combined
    )
    assert "Stage 15B — local/smeared path closure, Jacobi, and compensated-path checks" in combined


def test_stage15a_does_not_promote_later_stage_claims():
    combined = NOTES + "\n" + RESULT
    for phrase in (
        "declared Dirac-payload consistency != full Dirac-observable descent",
        "local/smeared closure != compensated local-path closure",
        "Stage 15A locality consistency != Stage 15D basis obstruction",
        "known nonlocal seed reconstruction != proof of locality-protected non-Abelianity",
        "finite smeared algebra != continuum hypersurface-deformation algebra",
        "spatially indexed constraint precursor != general relativity",
    ):
        assert phrase in combined


def test_stage15a_freeze_remains_historical_and_unchanged_in_role():
    assert "Stage 15.0 completed; criteria 1–10 satisfied; criteria 11–50 pending." in FREEZE
    assert "protocol preflight != Stage 15A scientific evidence" in FREEZE
    assert "known distance-2 seed reconstruction != proof that every Abelianization is nonlocal" in FREEZE

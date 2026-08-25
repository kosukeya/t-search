from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
NOTES=(ROOT/'docs'/'stage16b_notes.md').read_text(encoding='utf-8')
RESULT=(ROOT/'results'/'stage16b_paths.md').read_text(encoding='utf-8')
SCIENTIFIC_HEAD='5f7806f9cebcb0173d215c3795412c9ab384d8d9'


def test_stage16b_docs_record_scientific_checkpoint_and_counts():
    combined=NOTES+'\n'+RESULT
    for phrase in (
        SCIENTIFIC_HEAD,
        'PR run #2022',
        '1289 passed in 915.46s (0:15:15)',
        '2592 / 2592',
        '1296 / 1296',
        'presented_C_compensator_found_for_all_frozen_local_probes',
        '0.10279126289269715',
        '2268',
        '324',
        '7776 = 324×24',
        '7452 = 324×23',
        '0.015625',
        '0.03125',
    ):
        assert phrase in combined


def test_stage16b_docs_close_only_criteria_18_24_and_point_to_16c():
    combined=NOTES+'\n'+RESULT
    assert 'Criteria **25–50 remain pending**.' in combined
    assert 'Stage 16C — Dirac pair, four-clock complete relational observables, physical quotient, reachability, and orbit discrimination.' in combined
    for number in range(18,25):
        assert f'{number}.' in combined


def test_stage16b_docs_preserve_interpretation_guards():
    combined=NOTES+'\n'+RESULT
    for phrase in (
        'raw path-word inequality != physical path dependence',
        'seed-compensated closure != local presented-basis compensation',
        'presented compensator found != locality-preserving Abelianizing basis',
        'presented compensator not found in frozen word search != physical obstruction',
        'compensated cycle path closure != refoliation invariance',
        'cycle path defect != spacetime curvature',
        'finite constant smearing != continuum lapse/shift field',
        'Stage 16B path compensation != Stage 16D basis Abelianization',
        'repository validation != new scientific evidence',
    ):
        assert phrase in combined

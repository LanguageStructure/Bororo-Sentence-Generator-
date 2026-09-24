from bororo_generator.api import generate_record

def test_generated_record_exposes_evidence():
    r=generate_record("nudu",s_person="3SG")
    assert r["status"]=="generated"
    assert r["text"]=="unudure"
    assert r["evidence"]["reviewed_frame"]=="monovalent"
    assert r["evidence"]["reviewed_stem_class"]=="U"
    assert r["validation"]["accepted"]

def test_blocked_record_is_inspectable():
    r=generate_record("tawuje",a_person="2SG",o_person="3PL")
    assert r["status"]=="blocked"
    assert r["text"] is None
    assert r["evidence"]["reviewed_frame"]=="divalent"
    assert r["evidence"]["reviewed_stem_class"] is None


def test_api_exposes_layered_evidence():
    r=generate_record("nudu",s_person="3SG")
    assert r["evidence_layers"]["reviewed_grammar"]["morphology_license"]=={"type":"full_stem_class","stem_class":"U"}



def test_sparse_cell_keeps_legacy_class_null():
    r=generate_record("kodu",s_person="1SG")
    assert r["status"]=="generated"
    assert r["evidence"]["reviewed_stem_class"] is None
    assert r["evidence"]["reviewed_stem_class_legacy"] is True


def test_blocked_record_has_evidence_boundary():
    r=generate_record("tawuje",a_person="2SG",o_person="3PL")
    layers=r["evidence_layers"]
    assert layers["generated_candidate"]["status"]=="blocked"
    assert layers["generated_candidate"]["text"] is None
    assert layers["generated_candidate"]["reasons"]
    assert not layers["corpus_evidence"]["attested"]

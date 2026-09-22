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

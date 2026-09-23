from bororo_generator.paradigm_generation import paradigm_requests,generate_paradigm

def test_nudu_has_person_paradigm():
    req=paradigm_requests("nudu")
    assert len(req)==8
    rs=generate_paradigm("nudu")
    forms={r["request"]["s_person"]:r["text"] for r in rs}
    assert forms["1SG"]=="inudure"
    assert forms["3SG"]=="unudure"
    assert forms["3PL"]=="enudure"

def test_maku_crosses_only_reviewed_a_hosts_with_o_cells():
    req=paradigm_requests("maku")
    assert len(req)==6
    assert {"lemma":"maku","a_person":"2SG","o_person":"3PL"} in req
    assert {"lemma":"maku","a_person":"3SG","o_person":"3SG"} in req
    assert not any(r["a_person"]=="1SG" for r in req)
    assert {r["o_person"] for r in req}=={"3SG","3PL"}

def test_incomplete_evidence_has_no_paradigm():
    assert paradigm_requests("tawuje")==[]

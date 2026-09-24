from bororo_generator.experiment import ExperimentTask, proposal_from_task, score_bounded_proposal

def test_bounded_reviewed_request_generates():
    t=ExperimentTask("t1","nudu",s_person="1SG")
    p=proposal_from_task(t)
    s=score_bounded_proposal(t,p)
    assert not s.blocked
    assert s.condition=="evidence_bounded"

def test_bounded_missing_exact_cell_abstains():
    t=ExperimentTask("t2","meru",s_person="1SG")
    s=score_bounded_proposal(t,proposal_from_task(t))
    assert s.blocked
    assert "unsupported_but_plausible" in s.labels

def test_nonbaseline_construction_is_blocked_not_invented():
    t=ExperimentTask("t3","nudu",construction="subjunctive",s_person="1PL.EXCL")
    s=score_bounded_proposal(t,proposal_from_task(t))
    assert s.blocked
    assert s.generated_text is None

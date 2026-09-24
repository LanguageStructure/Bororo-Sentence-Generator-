from bororo_generator.experiment_scoring import score_direct_output, suffix_slot_conflict

def test_direct_output_requires_audit_not_inference():
    t={"task_id":"v1-001","lemma":"nudu"}
    r=score_direct_output(t,"inudure")
    assert "needs_linguistic_audit" in r["labels"]

def test_reviewed_suffix_conflict_is_detected_only_from_supplied_analysis():
    assert suffix_slot_conflict(["re","wo"])["violation"]
    assert not suffix_slot_conflict(["re"])["violation"]

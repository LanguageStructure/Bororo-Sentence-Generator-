from bororo_generator import evidence_queue

def test_queue_does_not_infer_missing_analysis(monkeypatch):
    class S:
        sent_id="s1"
        tokens=({"lemma":"x","form":"ix"},{"lemma":"x","form":"ex"})
    monkeypatch.setattr(evidence_queue,"read_conllu",lambda p:[S()])
    monkeypatch.setattr(evidence_queue,"reviewed_frame",lambda l:None)
    monkeypatch.setattr(evidence_queue,"reviewed_stem_class",lambda l:None)
    r=evidence_queue.lexical_evidence_queue("x")
    assert r[0]["needs"]==["coding_frame","stem_class"]
    assert "inferred_stem_class" not in r[0]

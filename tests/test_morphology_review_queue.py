from bororo_generator import morphology_review_queue as q

def test_queue_does_not_infer_analysis(monkeypatch):
    monkeypatch.setattr(q,"corpus_lemma_forms",lambda l,p:[
        {"form":"kodure","count":7,"sent_ids":["s1"],"upos":["VERB"],"deprels":["root"]}])
    rows=q.morphology_review_queue(["kodu"],"x")
    r=rows[0]
    assert r["review_state"]=="needs_human_review"
    assert r["inferred_person"] is None
    assert r["inferred_segmentation"] is None
    assert r["inferred_stem_class"] is None
    assert r["licenses_generation"] is False

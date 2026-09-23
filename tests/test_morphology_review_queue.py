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


def test_review_packet_preserves_analysis_boundary(monkeypatch):
    monkeypatch.setattr(q,"audit_lemma_contexts",lambda *a,**k:[
        {"sent_id":"s1","text":"X kodure","text_por":"...","form":"kodure",
         "upos":"VERB","deprel":"root","head":0}])
    p=q.review_packet("kodu","kodure","x")
    assert p["contexts"][0]["sent_id"]=="s1"
    assert p["analysis"]=={"person":None,"segmentation":None,"stem_class":None,"coding_frame":None}
    assert p["licenses_generation"] is False


def test_review_queue_summary_counts_workload_only():
    rows=[
        {"lemma":"kodu","form":"kodure","tokens":7,"review_state":"needs_human_review"},
        {"lemma":"kodu","form":"ikodu","tokens":2,"review_state":"exact_cell_reviewed"},
        {"lemma":"mako","form":"makore","tokens":4,"review_state":"needs_human_review"},
    ]
    s=q.review_queue_summary(rows)
    assert s["needs_human_review"]==2
    assert s["tokens_needing_review"]==11
    assert s["lemmas_needing_review"]==2

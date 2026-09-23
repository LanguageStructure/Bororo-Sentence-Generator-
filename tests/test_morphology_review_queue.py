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


def test_top_unresolved_preserves_priority_order():
    rows=[
        {"lemma":"kodu","form":"a","tokens":9,"review_state":"needs_human_review"},
        {"lemma":"mako","form":"b","tokens":4,"review_state":"needs_human_review"},
    ]
    s=q.review_queue_summary(rows)
    assert s["top_unresolved"][0]=={"lemma":"kodu","form":"a","tokens":9}


def test_reviewed_predicate_surfaces_are_construction_aware():
    mako=q.reviewed_predicate_surfaces("mako")
    assert "imagore" in mako
    assert "amagore" in mako
    assert "makore" in mako
    assert "imago" not in mako
    maku=q.reviewed_predicate_surfaces("maku")
    assert "maku" in maku
    assert "emaku" in maku

def test_unreviewed_surface_is_not_licensed_by_shape():
    assert "kodure" not in q.reviewed_predicate_surfaces("kodu")
    assert "ikodure" in q.reviewed_predicate_surfaces("kodu")


def test_full_class_does_not_blanket_license_unknown_surface(monkeypatch):
    monkeypatch.setattr(q,"corpus_lemma_forms",lambda lemma,path:[
        {"form":"unudure","count":1,"sent_ids":["s1"],"upos":["VERB"],"deprels":["root"]},
        {"form":"nuduUNKNOWN","count":1,"sent_ids":["s2"],"upos":["VERB"],"deprels":["root"]},
    ])
    rows=q.morphology_review_queue(["nudu"],"x")
    by_form={r["form"]:r for r in rows}
    assert by_form["unudure"]["review_state"]=="full_class_reviewed"
    assert by_form["nuduUNKNOWN"]["review_state"]=="needs_human_review"
    assert by_form["nuduUNKNOWN"]["licenses_generation"] is False


def test_surface_matching_ignores_textual_capitalization(monkeypatch):
    monkeypatch.setattr(q,"corpus_lemma_forms",lambda lemma,path:[
        {"form":"Ikodure","count":5,"sent_ids":["s1"],"upos":["VERB"],"deprels":["root"]},
    ])
    row=q.morphology_review_queue(["kodu"],"x")[0]
    assert row["form"]=="Ikodure"
    assert row["review_state"]=="exact_cell_reviewed"
    assert row["licenses_generation"] is True
    assert row["reviewed_requests"]==[{"lemma":"kodu","s_person":"1SG"}]
    assert row["match_type"]=="capitalization_variant"


def test_exact_surface_match_is_distinguished(monkeypatch):
    monkeypatch.setattr(q,"corpus_lemma_forms",lambda lemma,path:[
        {"form":"ikodure","count":1,"sent_ids":["s1"],"upos":["VERB"],"deprels":["root"]},
    ])
    row=q.morphology_review_queue(["kodu"],"x")[0]
    assert row["review_state"]=="exact_cell_reviewed"
    assert row["match_type"]=="exact_surface"


def test_mako_imperative_surface_is_reviewed_construction_cell(monkeypatch):
    monkeypatch.setattr(q,"corpus_lemma_forms",lambda lemma,path:[
        {"form":"tamagodo","count":3,"sent_ids":["s1"],"upos":["VERB"],"deprels":["ccomp"]},
        {"form":"Tamagodo","count":1,"sent_ids":["s2"],"upos":["VERB"],"deprels":["root"]},
    ])
    rows=q.morphology_review_queue(["mako"],"x")
    by_form={r["form"]:r for r in rows}
    assert by_form["tamagodo"]["review_state"]=="construction_cell_reviewed"
    assert by_form["tamagodo"]["match_type"]=="exact_surface"
    assert by_form["Tamagodo"]["match_type"]=="capitalization_variant"
    assert by_form["tamagodo"]["reviewed_construction_cells"]==[
        {"lemma":"mako","construction":"imperative","person":"2PL"}]

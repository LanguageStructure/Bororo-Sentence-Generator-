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
    assert "emagu" in maku

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


def test_construction_matching_is_not_imperative_specific(monkeypatch):
    monkeypatch.setitem(q.REVIEWED_CONSTRUCTION_CELLS,"dummy",{
        "other_construction":{"2SG":"DummyForm"}})
    monkeypatch.setattr(q,"corpus_lemma_forms",lambda lemma,path:[
        {"form":"DummyForm","count":1,"sent_ids":["s1"],"upos":["VERB"],"deprels":["root"]},
    ])
    row=q.morphology_review_queue(["dummy"],"x")[0]
    assert row["review_state"]=="construction_cell_reviewed"
    assert row["match_type"]=="exact_surface"
    assert row["reviewed_construction_cells"]==[
        {"lemma":"dummy","construction":"other_construction","person":"2SG"}]


def test_cegodure_matches_reviewed_kodu_1pl_exclusive(monkeypatch):
    monkeypatch.setattr(q,"corpus_lemma_forms",lambda lemma,path:[
        {"form":"Cegodure","count":2,"sent_ids":["7-2","556-4"],"upos":["VERB"],"deprels":["root"]},
    ])
    row=q.morphology_review_queue(["kodu"],"x")[0]
    assert row["review_state"]=="exact_cell_reviewed"
    assert row["match_type"]=="capitalization_variant"
    assert row["reviewed_requests"]==[{"lemma":"kodu","s_person":"1PL.EXCL"}]


def test_review_rows_expose_analysis_scope(monkeypatch):
    monkeypatch.setattr(q,"corpus_lemma_forms",lambda lemma,path:[
        {"form":"Cegodure","count":2,"sent_ids":["s1"],"upos":["VERB"],"deprels":["root"]},
    ])
    row=q.morphology_review_queue(["kodu"],"x")[0]
    assert row["analysis_scope"]=="exact_person_cell"

def test_construction_cell_has_construction_scope(monkeypatch):
    monkeypatch.setattr(q,"corpus_lemma_forms",lambda lemma,path:[
        {"form":"tamagodo","count":1,"sent_ids":["s1"],"upos":["VERB"],"deprels":["root"]},
    ])
    row=q.morphology_review_queue(["mako"],"x")[0]
    assert row["analysis_scope"]=="construction_cell"


def test_ikodumode_exposes_reviewed_operator_analysis(monkeypatch):
    monkeypatch.setattr(q,"corpus_lemma_forms",lambda lemma,path:[
        {"form":"ikodumode","count":2,"sent_ids":["43-2","46-2"],"upos":["VERB"],"deprels":["root","ccomp"]},
    ])
    row=q.morphology_review_queue(["kodu"],"x")[0]
    assert row["review_state"]=="construction_cell_reviewed"
    assert row["analysis_scope"]=="construction_cell"
    assert row["operator_analysis"]==["IRR","DECL"]
    assert row["reviewed_construction_cells"]==[
        {"lemma":"kodu","construction":"irrealis_declarative","person":"1SG"}]


def test_nonverbal_kodu_homograph_is_not_morphology_review(monkeypatch):
    monkeypatch.setattr(q,"corpus_lemma_forms",lambda lemma,path:[
        {"form":"kodu","count":2,"sent_ids":["37-2","67-1"],"upos":["NOUN"],"deprels":["nsubj","root"]},
    ])
    row=q.morphology_review_queue(["kodu"],"x")[0]
    assert row["review_state"]=="nonverbal_homograph"
    assert row["lexical_identity_status"]=="nonverbal_homograph"
    assert row["licenses_generation"] is False
    assert q.review_queue_summary([row])["needs_human_review"]==0


def test_mixed_upos_kodure_requires_token_identity_review(monkeypatch):
    monkeypatch.setattr(q,"corpus_lemma_forms",lambda lemma,path:[
        {"form":"kodure","count":2,"sent_ids":["91-2","110-5"],
         "upos":["NOUN","VERB"],"deprels":["root"]},
    ])
    row=q.morphology_review_queue(["kodu"],"x")[0]
    assert row["review_state"]=="token_identity_review"
    assert row["lexical_identity_status"]=="mixed_upos_requires_token_review"
    assert row["licenses_generation"] is False
    summary=q.review_queue_summary([row])
    assert summary["needs_human_review"]==1
    assert summary["token_identity_review"]==1


def test_cemerure_matches_reviewed_meru_1pl_exclusive(monkeypatch):
    monkeypatch.setattr(q,"corpus_lemma_forms",lambda lemma,path:[
        {"form":"Cemerure","count":2,"sent_ids":["51-5","51-8"],"upos":["VERB"],"deprels":["root"]},
    ])
    row=q.morphology_review_queue(["meru"],"x")[0]
    assert row["review_state"]=="exact_cell_reviewed"
    assert row["analysis_scope"]=="exact_person_cell"
    assert row["match_type"]=="capitalization_variant"
    assert row["reviewed_requests"]==[{"lemma":"meru","s_person":"1PL.EXCL"}]


def test_Akodudo_matches_kodu_imperative_cell(monkeypatch):
    monkeypatch.setattr(q,"corpus_lemma_forms",lambda lemma,path:[
        {"form":"Akodudo","count":1,"sent_ids":["45-2"],"upos":["VERB"],"deprels":["root"]},
    ])
    row=q.morphology_review_queue(["kodu"],"x")[0]
    assert row["review_state"]=="construction_cell_reviewed"
    assert row["analysis_scope"]=="construction_cell"
    assert row["match_type"]=="capitalization_variant"
    assert row["reviewed_construction_cells"]==[
        {"lemma":"kodu","construction":"imperative","person":"2SG"}]
    assert row["licenses_generation"] is True


def test_Ekodure_matches_reviewed_kodu_3pl(monkeypatch):
    monkeypatch.setattr(q,"corpus_lemma_forms",lambda lemma,path:[
        {"form":"Ekodure","count":1,"sent_ids":["5-2"],"upos":["VERB"],"deprels":["root"]},
    ])
    row=q.morphology_review_queue(["kodu"],"x")[0]
    assert row["review_state"]=="exact_cell_reviewed"
    assert row["analysis_scope"]=="exact_person_cell"
    assert row["match_type"]=="capitalization_variant"
    assert row["reviewed_requests"]==[{"lemma":"kodu","s_person":"3PL"}]


def test_Ikodui_matches_kodu_gerund_cell(monkeypatch):
    monkeypatch.setattr(q,"corpus_lemma_forms",lambda lemma,path:[
        {"form":"Ikodui","count":1,"sent_ids":["86-10"],"upos":["VERB"],"deprels":["root"]},
    ])
    row=q.morphology_review_queue(["kodu"],"x")[0]
    assert row["review_state"]=="construction_cell_reviewed"
    assert row["analysis_scope"]=="construction_cell"
    assert row["match_type"]=="capitalization_variant"
    assert row["reviewed_construction_cells"]==[
        {"lemma":"kodu","construction":"gerund","person":"1SG"}]


def test_Ikoduia_matches_kodu_optative_cell(monkeypatch):
    monkeypatch.setattr(q,"corpus_lemma_forms",lambda lemma,path:[
        {"form":"Ikoduia","count":1,"sent_ids":["41-4"],"upos":["VERB"],"deprels":["root"]},
    ])
    row=q.morphology_review_queue(["kodu"],"x")[0]
    assert row["review_state"]=="construction_cell_reviewed"
    assert row["analysis_scope"]=="construction_cell"
    assert row["match_type"]=="capitalization_variant"
    assert row["reviewed_construction_cells"]==[
        {"lemma":"kodu","construction":"optative","person":"1SG"}]


def test_Kodumodukare_matches_reviewed_construction_cell(monkeypatch):
    monkeypatch.setattr(q,"corpus_lemma_forms",lambda lemma,path:[
        {"form":"Kodumodukare","count":1,"sent_ids":["360-8"],"upos":["VERB"],"deprels":["advcl"]},
    ])
    row=q.morphology_review_queue(["kodu"],"x")[0]
    assert row["review_state"]=="construction_cell_reviewed"
    assert row["analysis_scope"]=="construction_cell"
    assert row["match_type"]=="capitalization_variant"
    assert row["reviewed_construction_cells"]==[
        {"lemma":"kodu","construction":"irrealis_negative_declarative","person":"3SG"}]


def test_ikoduwo_matches_kodu_subjunctive_cell(monkeypatch):
    monkeypatch.setattr(q,"corpus_lemma_forms",lambda lemma,path:[
        {"form":"ikoduwo","count":1,"sent_ids":["44-3"],"upos":["VERB"],"deprels":["xcomp"]},
    ])
    row=q.morphology_review_queue(["kodu"],"x")[0]
    assert row["review_state"]=="construction_cell_reviewed"
    assert row["analysis_scope"]=="construction_cell"
    assert row["match_type"]=="exact"
    assert row["reviewed_construction_cells"]==[
        {"lemma":"kodu","construction":"subjunctive","person":"1SG"}]

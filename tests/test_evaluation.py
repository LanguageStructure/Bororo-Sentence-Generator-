from bororo_generator import evaluation

def test_evaluation_does_not_equate_absence_with_failure(monkeypatch):
    monkeypatch.setattr(evaluation,"surface_attestation",lambda xs:{"unudure":["s1"]})
    monkeypatch.setattr(evaluation,"token_attestation",lambda xs:{})
    monkeypatch.setattr(evaluation,"read_conllu",lambda p:[])
    r=evaluation.evaluate_paradigm("nudu","dummy.conllu")
    assert r["generated_records"]==8
    assert r["structural_cells_sentence_attested"]==1
    assert r["unique_predicate_forms_attested"]==0
    assert "morphological evidence only" in r["interpretation"]

def test_multi_lexeme_summary(monkeypatch):
    monkeypatch.setattr(evaluation,"evaluate_paradigm",
        lambda l,p:{"lemma":l,"structural_cells_requested":8,
                    "structural_cells_sentence_attested":2,"generated_records":8,
                    "unique_predicate_forms_attested":3,"blocked":0,
                    "licensed_by_full_class":5,"licensed_by_exact_cell":3})
    r=evaluation.evaluate_lexemes(["nudu","meru"],"x")
    assert r["generated_records"]==16
    assert r["structural_cells_sentence_attested"]==4
    assert r["unique_predicate_forms_attested"]==6
    assert r["licensed_by_full_class"]==10
    assert r["licensed_by_exact_cell"]==6


def test_evaluation_exposes_separate_evidence_layers(monkeypatch):
    monkeypatch.setattr(evaluation,"read_conllu",lambda p:[])
    monkeypatch.setattr(evaluation,"surface_attestation",lambda xs:{})
    monkeypatch.setattr(evaluation,"token_attestation",lambda xs:{"inudure":["s1"]})
    r=evaluation.evaluate_paradigm("nudu","dummy.conllu")
    assert len(r["evidence_layers"])==r["structural_cells_requested"]
    layer=next(x for x in r["evidence_layers"]
               if x["generated_candidate"]["predicate_form"]=="inudure")
    assert layer["reviewed_grammar"]["reviewed_frame"]=="monovalent"
    assert layer["corpus_evidence"]["attested"]
    assert layer["corpus_evidence"]["sent_ids"]==["s1"]


def test_reviewed_construction_inventory():
    from bororo_generator.evaluation import reviewed_construction_inventory
    rows=reviewed_construction_inventory(["nudu","mako"])
    assert any(r["surface"]=="cenuduwo" and r["construction"]=="subjunctive" for r in rows)
    assert any(r["surface"]=="inudukare" and r["construction"]=="negative_indicative" for r in rows)
    assert any(r["surface"]=="tumagoi" and r["construction"]=="gerund" for r in rows)

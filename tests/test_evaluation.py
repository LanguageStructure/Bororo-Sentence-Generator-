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
                    "unique_predicate_forms_attested":3,"blocked":0})
    r=evaluation.evaluate_lexemes(["nudu","meru"],"x")
    assert r["generated_records"]==16
    assert r["structural_cells_sentence_attested"]==4
    assert r["unique_predicate_forms_attested"]==6

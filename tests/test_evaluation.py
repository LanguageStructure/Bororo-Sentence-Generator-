from bororo_generator import evaluation

def test_evaluation_does_not_equate_absence_with_failure(monkeypatch):
    monkeypatch.setattr(evaluation,"surface_attestation",lambda xs:{"unudure":["s1"]})
    monkeypatch.setattr(evaluation,"read_conllu",lambda p:[])
    r=evaluation.evaluate_paradigm("nudu","dummy.conllu")
    assert r["generated"]==8
    assert r["corpus_attested"]==1
    assert r["generated_unattested"]==7
    assert "absence is not evidence" in r["interpretation"]

def test_multi_lexeme_summary(monkeypatch):
    monkeypatch.setattr(evaluation,"evaluate_paradigm",
        lambda l,p:{"lemma":l,"cells_requested":8,"generated":8,
                    "corpus_attested":2,"generated_unattested":6,"blocked":0})
    r=evaluation.evaluate_lexemes(["nudu","meru"],"x")
    assert r["generated"]==16 and r["corpus_attested"]==4

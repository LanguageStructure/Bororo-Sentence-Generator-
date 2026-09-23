from bororo_generator import evaluation_report as er

def test_report_keeps_methodological_limits(monkeypatch):
    monkeypatch.setattr(er,"evaluate_lexemes",lambda ls,p:{
        "lexemes":1,"structural_cells_requested":8,
        "structural_cells_sentence_attested":0,"generated_records":8,
        "unique_predicate_forms_attested":2,"blocked":0,"results":[]})
    r=er.evaluation_report(["nudu"],"corpus.conllu")
    assert r["schema_version"]=="1.0"
    assert r["summary"]["generated_records"]==8
    assert any("not grammatical review" in x for x in r["method"]["limits"])

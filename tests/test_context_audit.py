from bororo_generator import context_audit

def test_context_audit_is_descriptive(monkeypatch):
    class S:
        sent_id="s1"; text="X"; translation_por="Y"
        tokens=({"lemma":"x","form":"ix","upos":"VERB","deprel":"root","head":0},)
    monkeypatch.setattr(context_audit,"read_conllu",lambda p:[S()])
    rows=context_audit.audit_lemma_contexts("c","x")
    assert rows[0]["form"]=="ix"
    assert set(rows[0])=={"sent_id","text","text_por","form","upos","deprel","head"}

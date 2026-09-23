from bororo_generator import corpus_evidence as ce

def test_corpus_observation_never_licenses_generation(monkeypatch):
    class S:
        sent_id="s1"
        tokens=({"lemma":"kodu","form":"kodure","upos":"VERB","deprel":"root"},)
    monkeypatch.setattr(ce,"read_conllu",lambda p:[S()])
    rows=ce.corpus_lemma_forms("kodu","x")
    assert rows[0]["form"]=="kodure"
    assert rows[0]["status"]=="corpus_observation"
    assert rows[0]["licenses_generation"] is False

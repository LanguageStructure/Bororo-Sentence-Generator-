from bororo_generator.evidence_resolver import resolve_lexeme
def test_sources_remain_separate():
    r=resolve_lexeme("aregodu",[{"entry":"aregodu","definition":"chegada, chegar","ipa":"/aregodu/"}])
    assert r.dictionary[0]["definition"]=="chegada, chegar"
    assert r.grammar.get("stem_class")=="O"
    assert "frame" not in r.grammar
def test_homography_blocks_generation():
    r=resolve_lexeme("kudu",[{"entry":"kudu","definition":"beber"},{"entry":"kudu","definition":"som"}])
    assert "dictionary_homography" in r.ambiguities
    assert not r.generation_ready
def test_reviewed_valency_can_be_ready_without_dictionary():
    r=resolve_lexeme("regodu")
    assert r.grammar["frame"]=="monovalent"
    assert r.generation_ready

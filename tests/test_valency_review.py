from bororo_generator.valency_review import reviewed_frame, generation_frame_ready
def test_reviewed_frames():
    assert reviewed_frame("regodu")=="monovalent"
    assert reviewed_frame("mako")=="extended_intransitive"
    assert reviewed_frame("tawuje")=="divalent"
    assert reviewed_frame("maku")=="divalent"
def test_unknown_valency_is_blocked():
    assert reviewed_frame("ako") is None
    assert not generation_frame_ready("ako")

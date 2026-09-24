from bororo_generator.lexical_review import review_status

def test_explicit_ambiguity_overrides_mechanical_missing_fields():
    assert review_status("tu",None,None)=="construction_ambiguity"

def test_pending_and_ready_states():
    assert review_status("x",None,"O")=="frame_pending"
    assert review_status("x","monovalent",None)=="stem_class_pending"
    assert review_status("x","monovalent","C")=="ready"

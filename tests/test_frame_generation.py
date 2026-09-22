from bororo_generator.frame_generation import monovalent_declarative

def test_nudu_reviewed_monovalent_u_class():
    c=monovalent_declarative("nudu","3SG")
    assert c is not None
    assert c.text=="unudure"

def test_aregodu_has_class_but_no_reviewed_frame():
    assert monovalent_declarative("aregodu","1SG") is None

def test_divalent_not_forced_into_monovalent_template():
    assert monovalent_declarative("tawuje","2SG") is None

def test_unknown_class_blocks_even_reviewed_frame():
    assert monovalent_declarative("regodu","3PL") is None

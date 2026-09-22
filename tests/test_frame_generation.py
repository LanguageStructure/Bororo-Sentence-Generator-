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


def test_meru_and_kodu_now_cross_morphology_and_valency_review():
    assert monovalent_declarative("meru","2SG").text=="amerure"
    assert monovalent_declarative("kodu","1SG").text=="ikodure"


def test_more_reviewed_c_class_roots():
    assert monovalent_declarative("maragodu","2PL").text=="tamaragodure"
    # mako and kudu are extended intransitives, so the monovalent declarative
    # generator must still refuse them despite their reviewed index class.
    assert monovalent_declarative("mako","2SG") is None
    assert monovalent_declarative("kudu","2SG") is None
    # maku is divalent and must likewise remain outside this generator.
    assert monovalent_declarative("maku","3PL") is None

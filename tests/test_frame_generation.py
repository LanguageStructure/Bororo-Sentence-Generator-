from bororo_generator.frame_generation import monovalent_indicative

def test_nudu_reviewed_monovalent_u_class():
    c=monovalent_indicative("nudu","3SG")
    assert c is not None
    assert c.text=="unudure"

def test_aregodu_has_class_but_no_reviewed_frame():
    assert monovalent_indicative("aregodu","1SG") is None

def test_divalent_not_forced_into_monovalent_template():
    assert monovalent_indicative("tawuje","2SG") is None

def test_unknown_class_blocks_even_reviewed_frame():
    assert monovalent_indicative("regodu","3PL") is None


def test_meru_and_kodu_now_cross_morphology_and_valency_review():
    assert monovalent_indicative("meru","2SG").text=="amerure"
    assert monovalent_indicative("kodu","1SG").text=="ikodure"


def test_more_reviewed_c_class_roots():
    assert monovalent_indicative("maragodu","2PL").text=="tamaragodure"
    # mako and kudu are extended intransitives, so the monovalent indicative
    # generator must still refuse them despite their reviewed index class.
    assert monovalent_indicative("mako","2SG") is None
    assert monovalent_indicative("kudu","2SG") is None
    # maku is divalent and must likewise remain outside this generator.
    assert monovalent_indicative("maku","3PL") is None


def test_sparse_cells_do_not_expand_to_unreviewed_persons():
    assert monovalent_indicative("meru","1SG") is None
    assert monovalent_indicative("kodu","3SG") is None
    assert monovalent_indicative("maragodu","1SG") is None

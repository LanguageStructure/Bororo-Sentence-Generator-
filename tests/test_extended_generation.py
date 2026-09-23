from bororo_generator.extended_generation import extended_intransitive_indicative

def test_mako_without_oblique():
    c=extended_intransitive_indicative("mako","2SG")
    assert c is not None
    assert c.text=="amagore"

def test_mako_with_reviewed_ji_oblique():
    c=extended_intransitive_indicative("mako","1SG","Boe")
    assert c is not None
    assert c.text=="imagore Boe ji"

def test_kudu_oblique_marker_is_not_guessed():
    assert extended_intransitive_indicative("kudu","2SG","poboce") is None

def test_divalent_maku_is_rejected():
    assert extended_intransitive_indicative("maku","3SG") is None


def test_sparse_extended_cells_do_not_expand():
    assert extended_intransitive_indicative("mako","3PL") is None
    assert extended_intransitive_indicative("kudu","1SG") is None

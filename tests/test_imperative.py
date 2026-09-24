from bororo_generator.imperative import positive_imperative, negative_imperative
def test_imperative_depends_on_frame():
    assert positive_imperative("monovalent")["suffix"]=="-do"
    assert positive_imperative("divalent")["suffix"] is None
    assert negative_imperative("monovalent")["pattern"]=="2=LEX-ka-ba"
    assert negative_imperative("divalent")["pattern"]=="2A=ka-ba O=LEX"


def test_reviewed_mako_2pl_imperative():
    from bororo_generator.imperative import reviewed_positive_imperative
    c=reviewed_positive_imperative("mako","2PL")
    assert c is not None
    assert c.text=="tamagodo"
    assert c.predicate_form=="tamagodo"

def test_reviewed_mako_2sg_imperative():
    from bororo_generator.imperative import reviewed_positive_imperative
    c=reviewed_positive_imperative("mako","2SG")
    assert c is not None
    assert c.text=="amagodo"
    assert c.predicate_form=="amagodo"

def test_mako_imperative_does_not_license_unreviewed_cells():
    from bororo_generator.imperative import reviewed_positive_imperative
    assert reviewed_positive_imperative("mako","1SG") is None

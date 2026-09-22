from bororo_generator.imperative import positive_imperative, negative_imperative
def test_imperative_depends_on_frame():
    assert positive_imperative("monovalent")["suffix"]=="-do"
    assert positive_imperative("divalent")["suffix"] is None
    assert negative_imperative("monovalent")["pattern"]=="2=LEX-ka-ba"
    assert negative_imperative("divalent")["pattern"]=="2A=ka-ba O=LEX"

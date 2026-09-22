from bororo_generator.morphotactics import ordering_licensed, ordering_violations
def test_directly_attested_order():
    assert ordering_licensed(["PERSON","LEX","IRR","NEG","DECL"])
    assert ordering_licensed(["LEX","ASPECT","DECL"])
    assert ordering_licensed(["LEX","IRR","NEG","QUOT"])
def test_reject_reversed_attested_relation():
    assert ("IRR","NEG") in ordering_violations(["LEX","NEG","IRR","DECL"])

from bororo_generator.morphotactics import ordering_licensed, ordering_violations
def test_directly_attested_order():
    assert ordering_licensed(["PERSON","LEX","IRR","NEG","DECL"])
    assert ordering_licensed(["LEX","ASPECT","DECL"])
    assert ordering_licensed(["LEX","IRR","NEG","QUOT"])
def test_reject_reversed_attested_relation():
    assert ("IRR","NEG") in ordering_violations(["LEX","NEG","IRR","DECL"])


def test_reviewed_irrealis_declarative_surface():
    from bororo_generator.morphotactics import reviewed_operator_surface,realize_irrealis_declarative
    assert reviewed_operator_surface("IRR","DECL")=="mode"
    assert realize_irrealis_declarative("ikodu")=="ikodumode"


def test_reviewed_irrealis_negative_declarative_surface():
    assert reviewed_operator_surface("IRR","NEG","DECL")=="modukare"

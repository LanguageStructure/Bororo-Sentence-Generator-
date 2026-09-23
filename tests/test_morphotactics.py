from bororo_generator.morphotactics import ordering_licensed, ordering_violations
def test_directly_attested_order():
    assert ordering_licensed(["PERSON","LEX","IRR","NEG","IND"])
    assert ordering_licensed(["LEX","ASPECT","IND"])
    assert ordering_licensed(["LEX","IRR","NEG","QUOT"])
def test_reject_reversed_attested_relation():
    assert ("IRR","NEG") in ordering_violations(["LEX","NEG","IRR","IND"])


def test_reviewed_irrealis_indicative_surface():
    from bororo_generator.morphotactics import reviewed_operator_surface,realize_irrealis_indicative
    assert reviewed_operator_surface("IRR","IND")=="mode"
    assert realize_irrealis_indicative("ikodu")=="ikodumode"


def test_reviewed_irrealis_negative_indicative_surface():
    from bororo_generator.morphotactics import reviewed_operator_surface
    assert reviewed_operator_surface("IRR","NEG","IND")=="modukare"

from bororo_generator.construction import construction
def test_reference_and_predication_are_constructions():
    assert construction("bare_reference").function=="reference"
    p=construction("declarative_predication")
    assert p.function=="predication"
    assert p.predicate_marking=="-re"
    assert p.person_realization=="bound_index"

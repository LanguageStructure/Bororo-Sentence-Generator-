from bororo_generator.coding_frame import coding_frame, declarative_schema

def test_s_o_alignment_location():
    assert coding_frame("monovalent").predicate_index_role=="S"
    assert coding_frame("divalent").predicate_index_role=="O"
    assert coding_frame("divalent").operator_host_role=="A"

def test_extended_intransitive_does_not_universalize_oblique_marker():
    f=coding_frame("extended_intransitive")
    assert f.core_roles==("S",)
    assert f.oblique_role=="additional_participant"
    assert f.oblique_marker is None
    assert "ji" not in declarative_schema("extended_intransitive")

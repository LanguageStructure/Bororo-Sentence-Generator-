from bororo_generator.coding_frame import coding_frame, declarative_schema
def test_s_o_alignment_location():
    assert coding_frame("monovalent").predicate_index_role=="S"
    assert coding_frame("divalent").predicate_index_role=="O"
    assert coding_frame("divalent").operator_host_role=="A"
def test_extended_intransitive_is_not_divalent():
    f=coding_frame("extended_intransitive")
    assert f.core_roles==("S",)
    assert f.oblique_marker=="ji"
    assert declarative_schema("extended_intransitive").endswith("RP ji")

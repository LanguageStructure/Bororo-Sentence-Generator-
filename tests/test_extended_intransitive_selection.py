from bororo_generator.coding_frame import coding_frame, declarative_schema
from bororo_generator.valency_review import reviewed_oblique

def test_extended_intransitive_has_no_universal_postposition():
    f=coding_frame("extended_intransitive")
    assert f.oblique_marker is None
    assert "POSTP" in declarative_schema("extended_intransitive")

def test_mako_has_reviewed_ji_selection():
    assert reviewed_oblique("mako")=="ji"

def test_kudu_does_not_inherit_ji():
    assert reviewed_oblique("kudu") is None

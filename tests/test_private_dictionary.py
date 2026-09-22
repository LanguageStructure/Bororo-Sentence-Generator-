from bororo_generator.private_dictionary import lookup_private
def test_homographs_are_preserved():
    rows=[{"entry":"kudu","definition":"drink"},{"entry":"kudu","definition":"sound"}]
    assert len(lookup_private(rows,"KUDU"))==2

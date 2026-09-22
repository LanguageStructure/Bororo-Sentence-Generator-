from bororo_generator.person_index import indexed_stem
def test_reviewed_stem_classes():
    assert indexed_stem("aregodu","1SG","O")=="itaregodu"
    assert indexed_stem("aregodu","2SG","O")=="akaregodu"
    assert indexed_stem("ogwa","1SG","N")=="inogwa"
    assert indexed_stem("ie","1SG","I")=="ikie"
def test_class_must_be_explicit():
    try: indexed_stem("ako","2SG","UNKNOWN")
    except ValueError: pass
    else: raise AssertionError("stem class must not be inferred")

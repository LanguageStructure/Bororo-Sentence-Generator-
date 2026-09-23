from bororo_generator.person_index import indexed_stem,indexed_reviewed_stem,reviewed_person_cell,reviewed_person_analysis
def test_reviewed_stem_classes():
    assert indexed_stem("aregodu","1SG","O")=="itaregodu"
    assert indexed_stem("aregodu","2SG","O")=="akaregodu"
    assert indexed_stem("ogwa","1SG","N")=="inogwa"
    assert indexed_stem("ie","1SG","I")=="ikie"
def test_class_must_be_explicit():
    try: indexed_stem("ako","2SG","UNKNOWN")
    except ValueError: pass
    else: raise AssertionError("stem class must not be inferred")

def test_reviewed_lexical_class_registry():
    from bororo_generator.person_index import reviewed_stem_class, indexed_reviewed_stem
    assert reviewed_stem_class("aregodu") == "O"
    assert indexed_reviewed_stem("aregodu","1SG") == "itaregodu"
    assert reviewed_stem_class("ako") is None
    assert indexed_reviewed_stem("ako","2SG") is None


def test_ogwa_n_class_exclusive_from_concrete_paradigm():
    assert indexed_reviewed_stem("ogwa","1PL.EXCL")=="ceogwa"


def test_sparse_review_does_not_become_full_stem_class():
    from bororo_generator.person_index import reviewed_stem_class, reviewed_person_cell
    assert reviewed_stem_class("kudu") is None
    assert reviewed_person_cell("kudu","2SG")=="akudu"
    assert indexed_reviewed_stem("kudu","2SG")=="akudu"
    assert indexed_reviewed_stem("kudu","3SG") is None

def test_representative_paradigm_remains_full_class():
    from bororo_generator.person_index import reviewed_stem_class
    assert reviewed_stem_class("nudu")=="U"
    assert indexed_reviewed_stem("nudu","3SG")=="unudu"


def test_kodu_reviewed_1pl_exclusive_cell():
    assert reviewed_person_cell("kodu","1PL.EXCL")=="cegodu"
    assert indexed_reviewed_stem("kodu","1PL.EXCL")=="cegodu"


def test_kodu_irrealis_declarative_cell_is_under_kodu():
    from bororo_generator.person_index import reviewed_construction_cell
    assert reviewed_construction_cell("kodu","irrealis_declarative","1SG")=="ikodumode"
    assert reviewed_construction_cell("mako","irrealis_declarative","1SG") is None


def test_emagu_preserves_underlying_e_plus_maku_analysis():
    assert reviewed_person_analysis("maku","3PL")=={
        "index":"e","lexeme":"maku","surface":"emagu"}
    assert reviewed_person_cell("maku","3PL")=="emagu"


def test_meru_reviewed_1pl_exclusive_cell():
    assert reviewed_person_cell("meru","1PL.EXCL")=="cemeru"
    assert indexed_reviewed_stem("meru","1PL.EXCL")=="cemeru"

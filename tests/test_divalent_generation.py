from bororo_generator.divalent_generation import divalent_declarative

def test_maku_zero_o():
    c=divalent_declarative("maku","3SG","3SG")
    assert c is not None
    assert c.text=="ure maku"

def test_maku_plural_o():
    c=divalent_declarative("maku","3PL","3PL")
    assert c is not None
    assert c.text=="ere emagu"

def test_overt_rps_keep_coding_positions():
    c=divalent_declarative("maku","3PL","3SG",overt_a="Ime",overt_o="pao")
    assert c.text=="Ime ere pao maku"

def test_nondivalent_rejected():
    assert divalent_declarative("nudu","3SG","3SG") is None

def test_divalent_without_reviewed_stem_class_stays_blocked():
    assert divalent_declarative("tawuje","2SG","3PL") is None


def test_unreviewed_a_host_is_blocked():
    assert divalent_declarative("maku","1SG","3SG") is None

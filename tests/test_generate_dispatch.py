from bororo_generator.generate import generate_indicative

def test_dispatch_monovalent():
    r=generate_indicative("nudu",s_person="3SG")
    assert not r.blocked and r.frame=="monovalent"
    assert r.candidate.text=="unudure"

def test_dispatch_extended():
    r=generate_indicative("mako",s_person="2SG",oblique_phrase="Boe")
    assert not r.blocked and r.frame=="extended_intransitive"
    assert r.candidate.text=="amagore Boe ji"

def test_dispatch_divalent():
    r=generate_indicative("maku",a_person="3PL",o_person="3PL")
    assert not r.blocked and r.frame=="divalent"
    assert r.candidate.text=="ere emagu"

def test_missing_role_is_explicitly_blocked():
    r=generate_indicative("maku",a_person="3PL")
    assert r.blocked and "A and O persons required" in r.reasons

def test_no_fallback_when_morphology_incomplete():
    r=generate_indicative("tawuje",a_person="2SG",o_person="3PL")
    assert r.blocked and r.frame=="divalent"
    assert r.candidate is None

def test_unknown_lexeme_is_blocked():
    r=generate_indicative("unknown",s_person="3SG")
    assert r.blocked and r.frame is None

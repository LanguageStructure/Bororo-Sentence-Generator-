from scripts.audit_attested_forms import _role_signature

def test_divalent_token_evidence_never_resolves_a():
    assert _role_signature("divalent",{"a_person":"2SG","o_person":"3PL"})=={
        "A":"UNRESOLVED","O":"3PL"
    }

def test_monovalent_signature_preserves_s():
    assert _role_signature("monovalent",{"s_person":"1SG"})["S"]=="1SG"

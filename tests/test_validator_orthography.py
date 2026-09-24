from bororo_generator.validator import validate_candidate
from bororo_generator.provenance import Provenance

def prov():
    return Provenance(status="generated",pattern="test",rules=["test"])

def test_validator_rejects_legacy_y():
    r=validate_candidate("tygo",prov())
    assert not r.accepted
    assert not r.checks["canonical_bororo_orthography"]

def test_validator_accepts_u_orthography():
    r=validate_candidate("tugo",prov())
    assert r.checks["canonical_bororo_orthography"]

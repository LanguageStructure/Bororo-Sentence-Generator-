import pytest
from bororo_generator.provenance import Provenance
from bororo_generator.validator import validate_candidate

def test_attested_requires_source():
    with pytest.raises(ValueError): Provenance(status="attested").validate()

def test_recombined_requires_substitution():
    with pytest.raises(ValueError):
        Provenance(status="recombined",source_sent_ids=["x"]).validate()

def test_generated_requires_rule_or_pattern():
    with pytest.raises(ValueError): Provenance(status="generated").validate()

def test_valid_attested():
    p=Provenance(status="attested",source_sent_ids=["BOR.1"])
    assert validate_candidate("example",p).accepted

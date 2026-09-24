from bororo_generator.candidate import Candidate
from bororo_generator.provenance import Provenance

def test_candidate_output_never_keeps_y():
    c=Candidate("Tygo y Y",Provenance(status="generated"))
    assert c.text=="Tugo u U"
    assert "y" not in c.text.casefold()

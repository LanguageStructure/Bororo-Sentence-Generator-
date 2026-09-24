from bororo_generator.morph_candidate import ako_candidate

def test_ako_candidate_has_generated_provenance():
 c=ako_candidate(person=1,number="Sing",mood="Ind",polarity="Neg")
 assert c is not None
 assert c.text=="inagokare"
 r=c.record()
 assert r["provenance"]["status"]=="generated"
 assert r["validation"]["accepted"]
 assert "experimental output" in r["validation"]["warnings"][0]

def test_reviewed_2sg_ind_candidate_is_licensed():
 c=ako_candidate(person=2,number="Sing",mood="Ind")
 assert c is not None
 assert c.text=="akagore"

def test_unreviewed_candidate_is_blocked():
 assert ako_candidate(person=2,number="Plur",mood="Ind") is None

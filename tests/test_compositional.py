from bororo_generator.compositional import realize_ako

def test_reviewed_ako_cells():
 assert realize_ako(person=1,number="Sing",mood="Ind")=="inagore"
 assert realize_ako(person=3,number="Sing",mood="Ind")=="akore"
 assert realize_ako(person=3,number="Plur",mood="Ind")=="egore"
 assert realize_ako(person=1,number="Sing",mood="Ind",polarity="Neg")=="inagokare"
 assert realize_ako(person=1,number="Plur",clusivity="Ex",mood="Ind")=="cenagore"
 assert realize_ako(person=3,number="Sing",mood="Ind",status="Irr")=="akomode"

def test_reviewed_nominal_possessive():
 assert realize_ako(person=1,number="Sing",usage="nominal_possessive")=="inago"
 assert realize_ako(person=3,number="Plur",usage="nominal_possessive")=="ego"

def test_unlicensed_cells_are_not_invented():
 assert realize_ako(person=2,number="Sing",mood="Ind") is None
 assert realize_ako(person=3,number="Sing",derivation="Cau") is None

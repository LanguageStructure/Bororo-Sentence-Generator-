from bororo_generator.generation_gate import check_lemmas,check_tokens

def test_gate(tmp_path):
 p=tmp_path/"r.yaml";p.write_text("lemmas:\n  ako:\n    status: approved\n  tu:\n    status: review_required\n",encoding="utf-8")
 g=check_lemmas(["ako"],p);assert g.allowed
 g=check_lemmas(["ako","tu"],p);assert not g.allowed and g.blocked_lemmas==["tu"]

def test_exact_cell_gate(tmp_path):
 p=tmp_path/"r.yaml"
 p.write_text("""lemmas:
  ako:
    status: partial
    approved_cells:
      - feats: {Mood: Ind, Number: Sing, Person: 1}
        form: inagore
""",encoding="utf-8")
 good=[{"id":1,"form":"inagore","lemma":"ako","upos":"NOUN","feats":{"Mood":"Ind","Number":"Sing","Person":"1"}}]
 bad=[{"id":1,"form":"inagokare","lemma":"ako","upos":"NOUN","feats":{"Mood":"Ind","Number":"Sing","Person":"1"}}]
 assert check_tokens(good,p).allowed
 assert not check_tokens(bad,p).allowed

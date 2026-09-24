from bororo_generator.review import generation_ready,approved_form,cell_generation_ready

def test_review_gate(tmp_path):
 p=tmp_path/"r.yaml";p.write_text("lemmas:\n  x:\n    status: approved\n",encoding="utf-8")
 assert generation_ready("x",p)
 assert not generation_ready("y",p)

def test_partial_cell_gate(tmp_path):
 p=tmp_path/"r.yaml"
 p.write_text("""lemmas:
  ako:
    status: partial
    approved_cells:
      - feats: {Mood: Ind, Number: Sing, Person: 1}
        form: inagore
""",encoding="utf-8")
 feats={"Mood":"Ind","Number":"Sing","Person":"1"}
 assert not generation_ready("ako",p)
 assert approved_form("ako",feats,p)=="inagore"
 assert cell_generation_ready("ako",feats,"Inagore",p)
 assert not cell_generation_ready("ako",feats,"inagokare",p)

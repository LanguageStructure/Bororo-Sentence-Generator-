from bororo_generator.review import load_review,generation_ready
def test_review_gate(tmp_path):
 p=tmp_path/"r.yaml";p.write_text("lemmas:\n  x:\n    status: approved\n",encoding="utf-8")
 assert generation_ready("x",p)
 assert not generation_ready("y",p)

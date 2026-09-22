from bororo_generator.generation_gate import check_lemmas
def test_gate(tmp_path):
 p=tmp_path/"r.yaml";p.write_text("lemmas:\n  ako:\n    status: approved\n  tu:\n    status: review_required\n",encoding="utf-8")
 g=check_lemmas(["ako"],p);assert g.allowed
 g=check_lemmas(["ako","tu"],p);assert not g.allowed and g.blocked_lemmas==["tu"]

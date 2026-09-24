from bororo_generator.corpus import read_conllu
from bororo_generator.readiness import assess_sentence
S="# sent_id = x\n# text = a b\n1\ta\ta\tVERB\t_\t_\t0\troot\t_\t_\n2\tb\tb\tVERB\t_\t_\t1\troot\t_\t_\n\n"
def test_stray_root_is_excluded(tmp_path):
 p=tmp_path/"x.conllu";p.write_text(S,encoding="utf-8")
 r=assess_sentence(list(read_conllu(p))[0])
 assert not r["trusted"]
 assert "root_deprel_nonzero_head" in r["reasons"]

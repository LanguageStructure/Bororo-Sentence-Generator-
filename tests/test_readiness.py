from bororo_generator.corpus import read_conllu
from bororo_generator.readiness import assess_sentence
SAMPLE="# sent_id = x\n# text = a b\n1\ta\ta\tNOUN\t_\t_\t2\tnsubj\t_\t_\n2\tb\tb\tVERB\t_\t_\t0\troot\t_\t_\n\n"
def test_good_sentence(tmp_path):
 p=tmp_path/"x.conllu";p.write_text(SAMPLE,encoding="utf-8")
 s=list(read_conllu(p))[0];assert assess_sentence(s)["trusted"]
def test_long_sentence(tmp_path):
 p=tmp_path/"x.conllu";p.write_text(SAMPLE,encoding="utf-8")
 s=list(read_conllu(p))[0];a=assess_sentence(s,max_tokens=1)
 assert not a["trusted"] and "too_long" in a["reasons"]

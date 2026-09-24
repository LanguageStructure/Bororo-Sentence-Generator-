from bororo_generator.corpus import read_conllu
from bororo_generator.slots import sentence_slots
S="# sent_id = x\n# text = foo runs\n1\tfoo\tfoo\tNOUN\t_\t_\t2\tnsubj\t_\t_\n2\truns\trun\tVERB\t_\t_\t0\troot\t_\t_\n\n"
def test_slots(tmp_path):
 p=tmp_path/"x.conllu";p.write_text(S,encoding="utf-8");s=list(read_conllu(p))[0]
 slots=sentence_slots(s)
 assert slots[0].lemma=="foo" and slots[0].head_lemma=="run"
 assert slots[1].form=="runs" and slots[1].head_lemma=="ROOT"

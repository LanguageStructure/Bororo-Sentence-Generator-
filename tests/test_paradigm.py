from bororo_generator.corpus import read_conllu
from bororo_generator.paradigm import descriptive_paradigm
S="# sent_id = x\n# text = Runs\n1\tRuns\trun\tVERB\t_\tPerson=3|Number=Sing\t0\troot\t_\t_\n\n"
def test_paradigm(tmp_path):
 p=tmp_path/"x.conllu";p.write_text(S,encoding="utf-8")
 d=descriptive_paradigm(list(read_conllu(p)),"run")
 assert list(d["cells"].values())[0]["runs"]==1

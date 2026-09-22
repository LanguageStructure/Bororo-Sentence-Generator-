from bororo_generator.corpus import read_conllu
from bororo_generator.morphology import morphology_inventory
S="# sent_id = x\n# text = foo runs\n1\tfoo\tfoo\tNOUN\t_\tNumber=Sing\t2\tnsubj\t_\t_\n2\truns\trun\tVERB\t_\tTense=Pres\t0\troot\t_\t_\n\n"
def test_inventory(tmp_path):
 p=tmp_path/"x.conllu";p.write_text(S,encoding="utf-8");inv=morphology_inventory(list(read_conllu(p)))
 assert inv["run"]["runs"]["Tense=Pres"]==1

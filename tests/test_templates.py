from bororo_generator.corpus import read_conllu
from bororo_generator.templates import from_sentence
S="# sent_id = x\n# text = foo runs\n1\tfoo\tfoo\tNOUN\t_\tNumber=Sing\t2\tnsubj\t_\t_\n2\truns\trun\tVERB\t_\t_\t0\troot\t_\t_\n\n"
def test_template_preserves_layers(tmp_path):
 p=tmp_path/"x.conllu";p.write_text(S,encoding="utf-8");s=list(read_conllu(p))[0]
 t=from_sentence(s)
 assert t.tokens[0].form=="foo" and t.tokens[0].lemma=="foo"
 assert t.tokens[0].deprel=="nsubj" and t.tokens[0].head==2
 assert t.tokens[0].feats["Number"]=="Sing"

from bororo_generator.corpus import read_conllu
from bororo_generator.recombine import recombine
S="# sent_id = a\n# text = foo runs\n1\tfoo\tfoo\tNOUN\t_\t_\t2\tnsubj\t_\t_\n2\truns\trun\tVERB\t_\t_\t0\troot\t_\t_\n\n# sent_id = b\n# text = bar walks\n1\tbar\tbar\tNOUN\t_\t_\t2\tnsubj\t_\t_\n2\twalks\twalk\tVERB\t_\t_\t0\troot\t_\t_\n\n"
def test_recombine(tmp_path):
 p=tmp_path/"x.conllu";p.write_text(S,encoding="utf-8");a,b=list(read_conllu(p))
 c=recombine(a,b,1,1)
 r=c.record()
 assert r["text"]=="bar runs"
 assert r["provenance"]["status"]=="recombined"
 assert r["validation"]["accepted"]

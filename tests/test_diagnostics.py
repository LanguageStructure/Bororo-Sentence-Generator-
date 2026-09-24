from bororo_generator.diagnostics import diagnose
SAMPLE="# sent_id = good\n# text = a b\n1\ta\ta\tNOUN\t_\t_\t2\tnsubj\t_\t_\n2\tb\tb\tVERB\t_\t_\t0\troot\t_\t_\n\n# sent_id = two-roots\n1\tx\tx\tVERB\t_\t_\t0\troot\t_\t_\n2\ty\ty\tVERB\t_\t_\t0\troot\t_\t_\n\n"
def test_diagnostics(tmp_path):
 p=tmp_path/"x.conllu";p.write_text(SAMPLE,encoding="utf-8");d=diagnose(p,long_threshold=10)
 assert d["summary"]["units"]==2
 assert d["summary"]["units_root_count_not_1"]==1
 assert d["units"][1]["roots"]==2

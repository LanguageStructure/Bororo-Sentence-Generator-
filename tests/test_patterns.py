from pathlib import Path
from bororo_generator.corpus import corpus_summary
from bororo_generator.patterns import extract_patterns
SAMPLE="# sent_id = s1\n# text = areme bito\n1\tareme\tareme\tNOUN\t_\t_\t2\tnsubj\t_\t_\n2\tbito\tbito\tVERB\t_\t_\t0\troot\t_\t_\n\n# sent_id = s2\n# text = imi bito\n1\timi\timi\tPRON\t_\t_\t2\tnsubj\t_\t_\n2\tbito\tbito\tVERB\t_\t_\t0\troot\t_\t_\n\n"
def test_summary_and_patterns(tmp_path:Path):
 p=tmp_path/"sample.conllu";p.write_text(SAMPLE,encoding="utf-8");s=corpus_summary(p);assert s["sentences"]==2 and s["tokens"]==4;assert len(extract_patterns(p))==2

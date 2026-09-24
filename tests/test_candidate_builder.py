from bororo_generator.corpus import read_conllu
from bororo_generator.candidate_builder import attested_candidate,generation_gate_for_sentence
S="# sent_id = x\n# text = foo.\n1\tfoo\tfoo\tNOUN\t_\t_\t0\troot\t_\t_\n2\t.\t.\tPUNCT\t_\t_\t1\tpunct\t_\t_\n\n"
def test_attested_and_gate(tmp_path):
 p=tmp_path/"x.conllu";p.write_text(S,encoding="utf-8");s=list(read_conllu(p))[0]
 c=attested_candidate(s);assert c.provenance.status=="attested"
 r=tmp_path/"r.yaml";r.write_text("lemmas:\n  foo:\n    status: approved\n",encoding="utf-8")
 assert generation_gate_for_sentence(s,r).allowed

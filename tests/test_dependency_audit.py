from bororo_generator.corpus import read_conllu
from bororo_generator.dependency_audit import audit_lemma_context
S="""# sent_id = x
# text = Akore boe.
1	Akore	ako	VERB	_	Mood=Ind|Number=Sing|Person=3	0	root	_	_
2	boe	boe	NOUN	_	Number=Sing	1	nsubj	_	_

"""
def test_audit(tmp_path):
 p=tmp_path/"x.conllu";p.write_text(S,encoding="utf-8")
 a=audit_lemma_context(read_conllu(p),"ako")
 assert a["akore"]["count"]==1
 assert a["akore"]["deprel"]["root"]==1
 assert any(k.startswith("nsubj|boe|NOUN|") for k in a["akore"]["dependents"])

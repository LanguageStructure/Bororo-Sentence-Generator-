from bororo_generator.corpus import read_conllu
from bororo_generator.template_generation import replace_ako_cell

S="""# sent_id = x
# text = Akore boe.
1	Akore	ako	VERB	_	Mood=Ind|Number=Sing|Person=3	0	root	_	_
2	boe	boe	NOUN	_	_	1	nsubj	_	_
3	.	.	PUNCT	_	_	1	punct	_	_

"""

def test_template_replacement_with_reviewed_cell(tmp_path):
 p=tmp_path/"x.conllu";p.write_text(S,encoding="utf-8")
 s=list(read_conllu(p))[0]
 c=replace_ako_cell(s,1,{"person":1,"number":"Sing","mood":"Ind"})
 assert c.text.startswith("inagore ")
 assert c.provenance.status=="generated"
 assert c.provenance.source_sent_ids==["x"]
 assert c.provenance.substitutions[0]["old_form"]=="Akore"
 assert c.provenance.substitutions[0]["new_form"]=="inagore"

def test_template_replacement_blocks_unknown_cell(tmp_path):
 p=tmp_path/"x.conllu";p.write_text(S,encoding="utf-8")
 s=list(read_conllu(p))[0]
 assert replace_ako_cell(s,1,{"person":2,"number":"Plur","mood":"Ind"}) is None

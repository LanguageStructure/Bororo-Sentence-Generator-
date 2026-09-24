#!/usr/bin/env python3
"""Find attested ako tokens and test reviewed morphology inside their templates."""
import json,sys
from bororo_generator.corpus import read_conllu
from bororo_generator.template_generation import replace_ako_cell

path=sys.argv[1] if len(sys.argv)>1 else "data/corbo/trusted.conllu"
shown=0
for s in read_conllu(path):
 for t in s.tokens:
  if str(t.get("lemma") or "")!="ako": continue
  c=replace_ako_cell(s,t["id"],{"person":1,"number":"Sing","mood":"Ind"})
  if c:
   print(json.dumps({"source":s.text,"candidate":c.record()},ensure_ascii=False,indent=2))
   shown+=1
  if shown>=5: raise SystemExit

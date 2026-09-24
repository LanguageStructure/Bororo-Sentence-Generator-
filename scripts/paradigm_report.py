#!/usr/bin/env python3
import argparse
from bororo_generator.corpus import read_conllu
from bororo_generator.readiness import assess_sentence
from bororo_generator.paradigm import descriptive_paradigm
def main():
 p=argparse.ArgumentParser();p.add_argument("conllu");p.add_argument("lemma");a=p.parse_args()
 ss=[s for s in read_conllu(a.conllu) if assess_sentence(s)["trusted"]]
 d=descriptive_paradigm(ss,a.lemma)
 print(f"Lemma: {a.lemma}\n")
 for feats,forms in sorted(d["cells"].items(),key=lambda x:-sum(x[1].values())):
  print(feats)
  for form,n in sorted(forms.items(),key=lambda x:-x[1]):
   print(f"  {form}: {n}")
   for e in d["examples"].get((feats,form),[])[:2]:print(f"    [{e['sent_id']}] {e['text']}")
if __name__=="__main__":main()

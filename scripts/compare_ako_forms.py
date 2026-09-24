#!/usr/bin/env python3
import argparse
from collections import Counter,defaultdict
from bororo_generator.corpus import read_conllu
from bororo_generator.readiness import assess_sentence
from bororo_generator.orthography import form_key
def main():
 p=argparse.ArgumentParser();p.add_argument("conllu");p.add_argument("--examples",type=int,default=4);a=p.parse_args();groups=defaultdict(list)
 for s in read_conllu(a.conllu):
  if not assess_sentence(s)["trusted"]:continue
  ints={t["id"]:t for t in s.tokens if isinstance(t.get("id"),int)}
  for t in ints.values():
   if str(t.get("lemma") or "_")=="ako":
    groups[form_key(t.get("form"))].append((s,t,[d for d in ints.values() if d.get("head")==t["id"]]))
 print(f"Analytical form groups: {len(groups)}")
 for key,items in sorted(groups.items(),key=lambda x:(-len(x[1]),x[0])):
  spell=Counter(str(t.get("form")) for _,t,_ in items);rel=Counter(str(t.get("deprel")) for _,t,_ in items);child=Counter(str(d.get("deprel")) for _,_,ds in items for d in ds);feats=Counter(str(t.get("feats") or "_") for _,t,_ in items)
  print(f"\n## {key}: {len(items)}");print("spellings: "+", ".join(f"{x}={n}" for x,n in spell.most_common()));print("DEPREL: "+", ".join(f"{x}={n}" for x,n in rel.most_common()));print("FEATS: "+", ".join(f"{x}={n}" for x,n in feats.most_common()));print("direct dependents: "+(", ".join(f"{x}={n}" for x,n in child.most_common()) or "none"))
  for s,t,_ in items[:a.examples]:print(f"  [{s.sent_id}] {s.text}")
if __name__=="__main__":main()

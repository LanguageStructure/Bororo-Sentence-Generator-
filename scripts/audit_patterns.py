#!/usr/bin/env python3
import argparse
from collections import defaultdict
from bororo_generator.corpus import read_conllu
from bororo_generator.readiness import assess_sentence
from bororo_generator.patterns import construction_signature,valency_signature

def clean_upos(x):
    if x is None:return "_"
    x=str(x).strip().upper()
    aliases={"VERB":"VERB","NOUN":"NOUN","NON":"NOUN"}
    return aliases.get(x,x)

def main():
    p=argparse.ArgumentParser(description="Audit construction and valency analyses with attested examples.")
    p.add_argument("conllu");p.add_argument("--top",type=int,default=30)
    p.add_argument("--examples",type=int,default=5)
    a=p.parse_args()
    ss=[s for s in read_conllu(a.conllu) if assess_sentence(s)["trusted"]]
    constructions=defaultdict(list);valencies=defaultdict(list);upos_variants=defaultdict(set)
    root_anomalies=[]
    for s in ss:
        for t in s.tokens:
            raw=t.get("upos")
            if raw: upos_variants[clean_upos(raw)].add(str(raw))
        constructions[construction_signature(s)].append(s)
        valencies[valency_signature(s)].append(s)
        roots=[t for t in s.tokens if t.get("head")==0 and t.get("deprel")=="root"]
        relroots=[t for t in s.tokens if t.get("deprel")=="root"]
        if len(relroots)!=len(roots):
            root_anomalies.append((s.sent_id,len(roots),len(relroots),s.text))
    print(f"Trusted units: {len(ss)}")
    print("\nUPOS variants:")
    for norm,raw in sorted(upos_variants.items()):
        if len(raw)>1 or norm in {"?","NOUN","VERB"}:
            print(f"  {norm} <- {sorted(raw)!r}")
    print(f"\nRoot-count anomalies (DEPREL=root but HEAD!=0): {len(root_anomalies)}")
    for x in root_anomalies[:a.examples]:print(f"  {x[0]} head0-root={x[1]} deprel-root={x[2]} | {x[3]}")
    print("\nCONSTRUCTIONS")
    for sig,items in sorted(constructions.items(),key=lambda kv:(-len(kv[1]),kv[0]))[:a.top]:
        print(f"\n{len(items)} × {sig}")
        for s in items[:a.examples]:print(f"  [{s.sent_id}] {s.text}")
    print("\nVALENCY")
    for sig,items in sorted(valencies.items(),key=lambda kv:(-len(kv[1]),kv[0]))[:a.top]:
        print(f"\n{len(items)} × {sig}")
        for s in items[:a.examples]:print(f"  [{s.sent_id}] {s.text}")

if __name__=="__main__":main()

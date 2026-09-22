#!/usr/bin/env python3
import argparse
from collections import Counter
from bororo_generator.corpus import read_conllu
from bororo_generator.readiness import assess_sentence
from bororo_generator.patterns import construction_signature,valency_signature

def main():
    p=argparse.ArgumentParser(description="Inspect a provisional trusted CoNLL-U subset.")
    p.add_argument("conllu");p.add_argument("--top",type=int,default=20)
    a=p.parse_args()
    ss=list(read_conllu(a.conllu))
    trusted=[s for s in ss if assess_sentence(s)["trusted"]]
    upos=Counter();rels=Counter();constructions=Counter();valency=Counter()
    for s in trusted:
        for t in s.tokens:
            if t.get("upos"): upos[str(t["upos"])]+=1
            if t.get("deprel"): rels[str(t["deprel"])]+=1
        constructions[construction_signature(s)]+=1
        valency[valency_signature(s)]+=1
    print(f"Parsed units: {len(ss)} | readiness-trusted: {len(trusted)}")
    print("\nUPOS:");print(*[f"{k}: {v}" for k,v in upos.most_common(a.top)],sep="\n")
    print("\nRelations:");print(*[f"{k}: {v}" for k,v in rels.most_common(a.top)],sep="\n")
    print("\nConstruction signatures:");print(*[f"{v} × {k}" for k,v in constructions.most_common(a.top)],sep="\n")
    print("\nValency signatures:");print(*[f"{v} × {k}" for k,v in valency.most_common(a.top)],sep="\n")

if __name__=="__main__":main()

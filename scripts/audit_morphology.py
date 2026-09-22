#!/usr/bin/env python3
import argparse
from bororo_generator.corpus import read_conllu
from bororo_generator.readiness import assess_sentence
from bororo_generator.morphology import morphology_inventory

def main():
    p=argparse.ArgumentParser(description="Show attested form/FEATS realizations for a lemma.")
    p.add_argument("conllu");p.add_argument("lemma")
    a=p.parse_args()
    ss=[s for s in read_conllu(a.conllu) if assess_sentence(s)["trusted"]]
    inv=morphology_inventory(ss).get(a.lemma,{})
    print(f"Lemma: {a.lemma}")
    if not inv: print("No attested tokens in trusted evidence.");return
    for form,features in sorted(inv.items(),key=lambda kv:(-sum(kv[1].values()),kv[0])):
        print(f"\n{form}: {sum(features.values())}")
        for feats,n in features.most_common():print(f"  {n} × {feats}")

if __name__=="__main__":main()

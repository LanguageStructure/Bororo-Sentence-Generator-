#!/usr/bin/env python3
import argparse
from bororo_generator.corpus import read_conllu
from bororo_generator.readiness import assess_sentence
from bororo_generator.morphology import morphology_inventory
from bororo_generator.review import lemma_review,generation_ready

def main():
    p=argparse.ArgumentParser(description="Compare corpus morphology with human-reviewed analyses.")
    p.add_argument("conllu");p.add_argument("lemma")
    a=p.parse_args()
    ss=[s for s in read_conllu(a.conllu) if assess_sentence(s)["trusted"]]
    inv=morphology_inventory(ss).get(a.lemma,{})
    review=lemma_review(a.lemma)
    print(f"Lemma: {a.lemma}")
    print(f"Generation-ready: {'yes' if generation_ready(a.lemma) else 'no'}")
    print(f"Review record: {review or 'none'}")
    print("\nAttested forms:")
    for form,fs in sorted(inv.items(),key=lambda kv:(-sum(kv[1].values()),kv[0])):
        print(f"  {form}: {sum(fs.values())} | FEATS: {dict(fs)}")

if __name__=="__main__":main()

#!/usr/bin/env python3
"""List internally inconsistent root annotations without modifying the corpus."""
import argparse
from bororo_generator.corpus import read_conllu

def main():
    p=argparse.ArgumentParser();p.add_argument("conllu");a=p.parse_args()
    n=0
    for s in read_conllu(a.conllu):
        bad=[t for t in s.tokens if isinstance(t.get("id"),int)
             and t.get("deprel")=="root" and t.get("head")!=0]
        if not bad:continue
        n+=1
        print(f"\n[{s.sent_id}] {s.text}")
        for t in bad:
            print(f"  id={t['id']} form={t.get('form')} lemma={t.get('lemma')} head={t.get('head')} deprel=root")
    print(f"\nUnits with inconsistent root annotation: {n}")

if __name__=="__main__":main()

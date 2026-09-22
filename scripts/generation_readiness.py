#!/usr/bin/env python3
import argparse
from collections import Counter
from bororo_generator.corpus import read_conllu
from bororo_generator.readiness import assess_sentence
from bororo_generator.generation_gate import check_lemmas

def main():
    p=argparse.ArgumentParser(description="Report which frequent lemmas are approved for generation.")
    p.add_argument("conllu");p.add_argument("--top",type=int,default=30)
    p.add_argument("--review",default="config/morphology_review.yaml")
    a=p.parse_args()
    ss=[s for s in read_conllu(a.conllu) if assess_sentence(s)["trusted"]]
    counts=Counter(str(t.get("lemma")) for s in ss for t in s.tokens
                   if isinstance(t.get("id"),int) and t.get("lemma") not in (None,"_"))
    print(f"Trusted units: {len(ss)}")
    print("\nFrequent lemmas and generation gate:")
    for lemma,n in counts.most_common(a.top):
        g=check_lemmas([lemma],a.review)
        print(f"  {lemma}: {n} | {'APPROVED' if g.allowed else 'REVIEW REQUIRED'}")
    allgate=check_lemmas([x for x,_ in counts.most_common(a.top)],a.review)
    print(f"\nApproved among top {min(a.top,len(counts))}: {min(a.top,len(counts))-len(allgate.blocked_lemmas)}")
    print(f"Blocked: {len(allgate.blocked_lemmas)}")

if __name__=="__main__":main()

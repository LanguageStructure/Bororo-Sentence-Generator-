#!/usr/bin/env python3
import argparse
from collections import Counter,defaultdict
from bororo_generator.corpus import read_conllu
from bororo_generator.readiness import assess_sentence
from bororo_generator.generation_gate import check_lemmas

# Punctuation is structural evidence, not a morphology-review target.
EXCLUDED_UPOS={"PUNCT"}

def main():
    p=argparse.ArgumentParser(description="Report frequent lexical lemmas requiring human morphology review.")
    p.add_argument("conllu");p.add_argument("--top",type=int,default=30)
    p.add_argument("--review",default="config/morphology_review.yaml")
    a=p.parse_args()
    ss=[s for s in read_conllu(a.conllu) if assess_sentence(s)["trusted"]]
    counts=Counter();upos=defaultdict(Counter);excluded=Counter()
    for s in ss:
        for t in s.tokens:
            if not isinstance(t.get("id"),int):continue
            lemma=t.get("lemma");u=str(t.get("upos") or "_").strip().upper()
            if lemma in (None,"_"):continue
            if u in EXCLUDED_UPOS:
                excluded[str(lemma)]+=1;continue
            counts[str(lemma)]+=1;upos[str(lemma)][u]+=1

    print(f"Trusted units: {len(ss)}")
    print(f"Excluded punctuation tokens: {sum(excluded.values())}")
    print("\nFrequent lexical lemmas and generation gate:")
    selected=counts.most_common(a.top)
    for lemma,n in selected:
        g=check_lemmas([lemma],a.review)
        tags=",".join(x for x,_ in upos[lemma].most_common())
        print(f"  {lemma}: {n} | UPOS={tags} | {'APPROVED' if g.allowed else 'REVIEW REQUIRED'}")
    allgate=check_lemmas([x for x,_ in selected],a.review)
    print(f"\nApproved among top {len(selected)} lexical lemmas: {len(selected)-len(allgate.blocked_lemmas)}")
    print(f"Blocked: {len(allgate.blocked_lemmas)}")

if __name__=="__main__":main()

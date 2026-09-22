#!/usr/bin/env python3
"""Audit frequent non-punctuation lemmas before any morphology is approved."""
import argparse
from collections import Counter,defaultdict
from bororo_generator.corpus import read_conllu
from bororo_generator.readiness import assess_sentence

def main():
    p=argparse.ArgumentParser()
    p.add_argument("conllu");p.add_argument("--top",type=int,default=30)
    p.add_argument("--examples",type=int,default=3)
    a=p.parse_args()
    ss=[s for s in read_conllu(a.conllu) if assess_sentence(s)["trusted"]]
    freq=Counter(); info=defaultdict(lambda:{"forms":Counter(),"upos":Counter(),"deps":Counter(),"examples":[]})
    for s in ss:
        for t in s.tokens:
            if not isinstance(t.get("id"),int): continue
            upos=str(t.get("upos") or "_").strip().upper()
            lemma=str(t.get("lemma") or "_")
            if lemma=="_" or upos=="PUNCT": continue
            freq[lemma]+=1
            d=info[lemma];d["forms"][str(t.get("form") or "_")]+=1;d["upos"][upos]+=1;d["deps"][str(t.get("deprel") or "_")]+=1
            if len(d["examples"])<a.examples and s.sent_id not in {x[0] for x in d["examples"]}:
                d["examples"].append((s.sent_id,s.text))
    for lemma,n in freq.most_common(a.top):
        d=info[lemma]
        forms=", ".join(f"{x}({c})" for x,c in d["forms"].most_common(8))
        upos=", ".join(f"{x}:{c}" for x,c in d["upos"].most_common())
        deps=", ".join(f"{x}:{c}" for x,c in d["deps"].most_common(8))
        print(f"\n## {lemma} — {n}")
        print(f"UPOS: {upos}\nForms: {forms}\nDEPREL: {deps}")
        for sid,text in d["examples"]: print(f"  [{sid}] {text}")

if __name__=="__main__":main()

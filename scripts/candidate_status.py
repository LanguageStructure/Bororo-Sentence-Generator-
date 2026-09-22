#!/usr/bin/env python3
import argparse
from bororo_generator.corpus import read_conllu
from bororo_generator.readiness import assess_sentence
from bororo_generator.candidate_builder import generation_gate_for_sentence

def main():
    p=argparse.ArgumentParser(description="Show why trusted sentences are or are not ready to seed generation.")
    p.add_argument("conllu");p.add_argument("--limit",type=int,default=20)
    p.add_argument("--review",default="config/morphology_review.yaml")
    a=p.parse_args();shown=0
    for s in read_conllu(a.conllu):
        if not assess_sentence(s)["trusted"]:continue
        g=generation_gate_for_sentence(s,a.review)
        print(f"[{s.sent_id}] {'READY' if g.allowed else 'BLOCKED'}")
        print(f"  {s.text}")
        if g.blocked_lemmas:print("  review required: "+", ".join(g.blocked_lemmas))
        shown+=1
        if shown>=a.limit:break

if __name__=="__main__":main()

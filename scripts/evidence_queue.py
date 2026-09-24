#!/usr/bin/env python3
import argparse
from bororo_generator.evidence_queue import lexical_evidence_queue

def main():
    p=argparse.ArgumentParser(description="List corpus lexemes needing independent structural review")
    p.add_argument("corpus"); p.add_argument("--limit",type=int,default=25)
    p.add_argument("--minimum-tokens",type=int,default=2)
    a=p.parse_args()
    rows=lexical_evidence_queue(a.corpus,a.minimum_tokens)[:a.limit]
    print("lemma\ttokens\tforms\tstatus\tneeds\ttop_forms")
    for r in rows:
        forms=", ".join(f"{f}:{n}" for f,n in r["top_forms"])
        print(f'{r["lemma"]}\t{r["tokens"]}\t{r["distinct_forms"]}\t{r["review_status"]}\t{",".join(r["needs"])}\t{forms}')
if __name__=="__main__": main()

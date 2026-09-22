#!/usr/bin/env python3
import argparse
from bororo_generator.context_audit import audit_lemma_contexts,audit_summary

def main():
    p=argparse.ArgumentParser(description="Inspect corpus contexts before lexical review")
    p.add_argument("corpus"); p.add_argument("lemmas",nargs="+")
    p.add_argument("--limit",type=int,default=12)
    a=p.parse_args()
    for lemma in a.lemmas:
        rows=audit_lemma_contexts(a.corpus,lemma,a.limit)
        s=audit_summary(rows)
        print(f"\n## {lemma} | occurrences shown={s['occurrences']}")
        print("forms:",", ".join(f"{x}:{n}" for x,n in s["forms"]))
        print("relations:",", ".join(f"{x}:{n}" for x,n in s["deprel"]))
        for r in rows:
            tr=f" | PT: {r['text_por']}" if r["text_por"] else ""
            print(f"[{r['sent_id']}] {r['form']} <{r['upos']},{r['deprel']}> :: {r['text']}{tr}")
if __name__=="__main__": main()

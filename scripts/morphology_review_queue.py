#!/usr/bin/env python3
import argparse,json
from pathlib import Path
from bororo_generator.morphology_review_queue import morphology_review_queue,review_packet

def main():
    p=argparse.ArgumentParser(description="Rank corpus-observed forms for human morphology review")
    p.add_argument("corpus"); p.add_argument("lemmas",nargs="+")
    p.add_argument("--output")
    p.add_argument("--limit",type=int,default=50)
    p.add_argument("--contexts",type=int,default=0,help="Include up to N corpus contexts for each needs-review form")
    p.add_argument("--needs-only",action="store_true",help="Print/write only unresolved forms requiring human review")
    a=p.parse_args()
    rows=morphology_review_queue(a.lemmas,a.corpus)
    if a.needs_only:
        rows=[r for r in rows if r["review_state"]=="needs_human_review"]
    if a.contexts:
        for r in rows:
            if r["review_state"]=="needs_human_review":
                r["review_packet"]=review_packet(r["lemma"],r["form"],a.corpus,a.contexts)
    if a.output:
        out=Path(a.output); out.parent.mkdir(parents=True,exist_ok=True)
        out.write_text(json.dumps(rows,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
        print("report:",out)
    print("lemma\tform\ttokens\treview_state\tsent_ids")
    for r in rows[:a.limit]:
        print(f'{r["lemma"]}\t{r["form"]}\t{r["tokens"]}\t{r["review_state"]}\t{",".join(r["sent_ids"][:5])}')
if __name__=="__main__": main()

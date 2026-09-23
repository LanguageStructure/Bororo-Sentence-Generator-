#!/usr/bin/env python3
import argparse,json
from pathlib import Path
from bororo_generator.morphology_review_queue import morphology_review_queue

def main():
    p=argparse.ArgumentParser(description="Rank corpus-observed forms for human morphology review")
    p.add_argument("corpus"); p.add_argument("lemmas",nargs="+")
    p.add_argument("--output")
    p.add_argument("--limit",type=int,default=50)
    a=p.parse_args()
    rows=morphology_review_queue(a.lemmas,a.corpus)
    if a.output:
        out=Path(a.output); out.parent.mkdir(parents=True,exist_ok=True)
        out.write_text(json.dumps(rows,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
        print("report:",out)
    print("lemma\tform\ttokens\treview_state\tsent_ids")
    for r in rows[:a.limit]:
        print(f'{r["lemma"]}\t{r["form"]}\t{r["tokens"]}\t{r["review_state"]}\t{",".join(r["sent_ids"][:5])}')
if __name__=="__main__": main()

#!/usr/bin/env python3
import argparse,json
from pathlib import Path
from bororo_generator.morphology_review_queue import morphology_review_queue,review_packet,review_queue_summary

def main():
    p=argparse.ArgumentParser(description="Rank corpus-observed forms for human morphology review")
    p.add_argument("corpus"); p.add_argument("lemmas",nargs="+")
    p.add_argument("--output")
    p.add_argument("--limit",type=int,default=50)
    p.add_argument("--contexts",type=int,default=0,help="Include up to N corpus contexts for each needs-review form")
    p.add_argument("--needs-only",action="store_true",help="Print/write only unresolved forms requiring human review")
    p.add_argument("--next-only",action="store_true",help="Return only the highest-priority unresolved form with its review packet")
    p.add_argument("--reviewed-only",action="store_true",help="Print/write only corpus forms already matched to reviewed generated surfaces")
    a=p.parse_args()
    rows=morphology_review_queue(a.lemmas,a.corpus)
    if a.needs_only or a.next_only:
        rows=[r for r in rows if r["review_state"]=="needs_human_review"]
    elif a.reviewed_only:
        rows=[r for r in rows if r["review_state"] in {"construction_cell_reviewed","exact_cell_reviewed","full_class_reviewed"}]
    if a.next_only:
        rows=rows[:1]
    if a.next_only and not a.contexts:
        a.contexts=12
    if a.contexts:
        for r in rows:
            if r["review_state"]=="needs_human_review":
                r["review_packet"]=review_packet(r["lemma"],r["form"],a.corpus,a.contexts)
    summary=review_queue_summary(rows)
    if a.output:
        out=Path(a.output); out.parent.mkdir(parents=True,exist_ok=True)
        payload={"summary":summary,"rows":rows}
        out.write_text(json.dumps(payload,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
        print("report:",out)
    print("observed_forms:",summary["observed_forms"])
    print("needs_human_review:",summary["needs_human_review"])
    print("tokens_needing_review:",summary["tokens_needing_review"])
    print("lemmas_needing_review:",summary["lemmas_needing_review"])
    print("lemma\tform\ttokens\treview_state\tmatch_type\tsent_ids")
    for r in rows[:a.limit]:
        print(f'{r["lemma"]}\t{r["form"]}\t{r["tokens"]}\t{r["review_state"]}\t{r.get("match_type") or "-"}\t{",".join(r["sent_ids"][:5])}')
        if a.next_only and r.get("review_packet"):
            for x in r["review_packet"]["contexts"]:
                tr=f' | PT: {x["text_por"]}' if x.get("text_por") else ""
                print(f'  [{x["sent_id"]}] {x["form"]} <{x["upos"]},{x["deprel"]}> :: {x["text"]}{tr}')
if __name__=="__main__": main()

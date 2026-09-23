#!/usr/bin/env python3
"""Compare direct LLM surfaces with the frozen v1 controlled realization.

Exact-match is deliberately conservative. It does not infer segmentation or
promote experimental outputs into the reviewed grammar.
"""
import argparse,json,re
from pathlib import Path
from bororo_generator.experiment import ExperimentTask,proposal_from_task,score_bounded_proposal

TASK_FIELDS=("task_id","lemma","construction","s_person","a_person","o_person","oblique_phrase")

def task_obj(d):
    return ExperimentTask(**{k:d.get(k) for k in TASK_FIELDS})

def norm(s):
    # Comparison normalization only: trim/collapse whitespace and terminal punctuation.
    s=re.sub(r"\s+"," ",(s or "").strip())
    return s.rstrip(".!?").strip()

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument("direct_collected")
    ap.add_argument("--output",required=True)
    a=ap.parse_args()
    rows=[json.loads(x) for x in Path(a.direct_collected).read_text(encoding="utf8").splitlines() if x.strip()]
    out=Path(a.output); out.parent.mkdir(parents=True,exist_ok=True)
    exact=nonmatch=blocked=0
    with out.open("w",encoding="utf8") as fh:
        for row in rows:
            task=task_obj(row["task"])
            bounded=score_bounded_proposal(task,proposal_from_task(task))
            surface=row["response"].get("surface","")
            expected=bounded.generated_text
            match=(not bounded.blocked and norm(surface)==norm(expected))
            if bounded.blocked: blocked+=1
            elif match: exact+=1
            else: nonmatch+=1
            rec={
              "task_id":task.task_id,
              "lemma":task.lemma,
              "frame":row["task"].get("frame"),
              "direct_surface":surface,
              "controlled_surface":expected,
              "exact_match":match,
              "controlled_blocked":bounded.blocked,
              "controlled_labels":bounded.labels,
              "note":"Exact surface comparison is not a complete grammaticality judgment.",
            }
            fh.write(json.dumps(rec,ensure_ascii=False)+"\n")
    print(f"rows: {len(rows)}")
    print(f"exact_matches: {exact}")
    print(f"nonmatches: {nonmatch}")
    print(f"controlled_blocked: {blocked}")
    print(f"output: {out}")

if __name__=="__main__": main()

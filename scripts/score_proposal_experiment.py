#!/usr/bin/env python3
"""Score collected proposal-condition outputs with the frozen v1 reviewed grammar."""
import argparse,json
from pathlib import Path
from bororo_generator.experiment import ExperimentTask,StructuralProposal,score_bounded_proposal,record

TASK_FIELDS=("task_id","lemma","construction","s_person","a_person","o_person","oblique_phrase")
PROPOSAL_FIELDS=("lemma","construction","s_person","a_person","o_person","oblique_phrase")

def pick(d,fields): return {k:d.get(k) for k in fields}

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument("collected_jsonl")
    ap.add_argument("--output",required=True)
    a=ap.parse_args()
    rows=[json.loads(x) for x in Path(a.collected_jsonl).read_text(encoding="utf8").splitlines() if x.strip()]
    out=Path(a.output); out.parent.mkdir(parents=True,exist_ok=True)
    generated=blocked=0
    with out.open("w",encoding="utf8") as fh:
        for row in rows:
            if row.get("condition")!="proposal": raise SystemExit("expected proposal condition")
            task=ExperimentTask(**pick(row["task"],TASK_FIELDS))
            response=row["response"]
            proposal=StructuralProposal(**pick(response,PROPOSAL_FIELDS))
            score=score_bounded_proposal(task,proposal)
            rec=record(task,proposal,score)
            rec["run_metadata"]=row.get("run_metadata",{})
            fh.write(json.dumps(rec,ensure_ascii=False)+"\n")
            if score.blocked: blocked+=1
            else: generated+=1
    print(f"rows: {len(rows)}")
    print(f"generated: {generated}")
    print(f"blocked: {blocked}")
    print(f"output: {out}")

if __name__=="__main__": main()

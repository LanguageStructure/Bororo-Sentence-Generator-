#!/usr/bin/env python3
"""Audit whether condition-B structural proposals preserve the requested task.

This is evaluator-side validation only. It does not modify the frozen grammar
or the collected model outputs.
"""
import argparse,json
from collections import Counter
from pathlib import Path

FIELDS=("lemma","construction","s_person","a_person","o_person","oblique_phrase")

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument("collected")
    ap.add_argument("--output",required=True)
    a=ap.parse_args()
    rows=[json.loads(x) for x in Path(a.collected).read_text(encoding="utf8").splitlines() if x.strip()]
    out=[]
    for row in rows:
        task=row["task"]
        proposal=row.get("response") or row.get("parsed") or row.get("proposal")
        if not isinstance(proposal,dict):
            raise SystemExit(f"{task['task_id']}: missing parsed proposal")
        mismatches={}
        for field in FIELDS:
            expected=task.get(field)
            actual=proposal.get(field)
            if expected != actual:
                mismatches[field]={"expected":expected,"actual":actual}
        out.append({
          "task_id":task["task_id"],
          "aligned":not mismatches,
          "mismatches":mismatches,
          "task":task,
          "proposal":proposal,
        })
    p=Path(a.output); p.parent.mkdir(parents=True,exist_ok=True)
    p.write_text("\n".join(json.dumps(x,ensure_ascii=False) for x in out)+"\n",encoding="utf8")
    aligned=sum(x["aligned"] for x in out)
    fields=Counter(k for x in out for k in x["mismatches"])
    print(f"rows: {len(out)}")
    print(f"fully_aligned: {aligned}")
    print(f"task_mismatch: {len(out)-aligned}")
    print(f"mismatch_fields: {dict(fields)}")
    print(f"output: {p}")

if __name__=="__main__": main()

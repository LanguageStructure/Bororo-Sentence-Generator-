#!/usr/bin/env python3
"""Prepare a conservative human-audit worksheet for direct-condition nonmatches.

This script does not infer linguistic error types. It pre-fills only mechanical
facts established by the frozen controlled comparison and leaves linguistic
labels unresolved for human review.
"""
import argparse,csv,json
from pathlib import Path

FIELDS=[
 "task_id","lemma","frame","s_person","a_person","o_person",
 "direct_surface","controlled_surface","exact_match",
 "morphological_violation","frame_violation",
 "constructional_overgeneralization","complementary_distribution_violation",
 "unsupported_but_plausible","auditor_status","notes"
]

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument("direct_collected")
    ap.add_argument("comparison")
    ap.add_argument("--output",required=True)
    a=ap.parse_args()
    direct=[json.loads(x) for x in Path(a.direct_collected).read_text(encoding="utf8").splitlines() if x.strip()]
    comp=[json.loads(x) for x in Path(a.comparison).read_text(encoding="utf8").splitlines() if x.strip()]
    by_id={x["task_id"]:x for x in comp}
    out=Path(a.output); out.parent.mkdir(parents=True,exist_ok=True)
    pending=0
    with out.open("w",encoding="utf8",newline="") as fh:
        w=csv.DictWriter(fh,fieldnames=FIELDS,delimiter="\t"); w.writeheader()
        for row in direct:
            t=row["task"]; tid=t["task_id"]; c=by_id[tid]
            match=bool(c["exact_match"])
            if not match: pending+=1
            w.writerow({
              "task_id":tid,"lemma":t["lemma"],"frame":t.get("frame",""),
              "s_person":t.get("s_person") or "","a_person":t.get("a_person") or "",
              "o_person":t.get("o_person") or "",
              "direct_surface":c["direct_surface"],"controlled_surface":c["controlled_surface"],
              "exact_match":"yes" if match else "no",
              "morphological_violation":"no" if match else "unresolved",
              "frame_violation":"no" if match else "unresolved",
              "constructional_overgeneralization":"no" if match else "unresolved",
              "complementary_distribution_violation":"no" if match else "unresolved",
              "unsupported_but_plausible":"no" if match else "unresolved",
              "auditor_status":"reviewed" if match else "pending",
              "notes":"exact frozen-v1 surface match" if match else "",
            })
    print(f"rows: {len(direct)}")
    print(f"exact_reviewed: {len(direct)-pending}")
    print(f"pending_human_audit: {pending}")
    print(f"output: {out}")

if __name__=="__main__": main()

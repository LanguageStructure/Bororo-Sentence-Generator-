#!/usr/bin/env python3
"""Apply explicit human audit decisions without changing the frozen grammar.

Decisions live in a separate TSV so experimental judgments remain distinct from
the grammar and from mechanically prepared audit rows.
"""
import argparse,csv
from pathlib import Path

KEY="task_id"
DECISION_FIELDS=[
 "morphological_violation","construction_mismatch",
 "s_person_mismatch","a_person_mismatch","o_person_mismatch","frame_violation",
 "constructional_overgeneralization","complementary_distribution_violation",
 "unsupported_but_plausible","auditor_status","notes",
]
ALLOWED={"yes","no","unresolved","not_applicable"}

def read_tsv(path):
    with Path(path).open(encoding="utf8",newline="") as f:
        return list(csv.DictReader(f,delimiter="\t"))

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument("audit")
    ap.add_argument("decisions")
    ap.add_argument("--output",required=True)
    a=ap.parse_args()
    rows=read_tsv(a.audit); decisions=read_tsv(a.decisions)
    by_id={r[KEY]:r for r in decisions}
    if len(by_id)!=len(decisions):
        raise SystemExit("duplicate task_id in decisions")
    known={r[KEY] for r in rows}
    unknown=set(by_id)-known
    if unknown: raise SystemExit(f"unknown task_id(s): {sorted(unknown)}")
    applied=0
    for r in rows:
        d=by_id.get(r[KEY])
        if not d: continue
        for field in DECISION_FIELDS:
            val=(d.get(field) or "").strip()
            if not val: continue
            if field not in {"notes","auditor_status"} and val not in ALLOWED:
                raise SystemExit(f"{r[KEY]}: invalid {field}={val!r}")
            r[field]=val
        applied+=1
    out=Path(a.output); out.parent.mkdir(parents=True,exist_ok=True)
    with out.open("w",encoding="utf8",newline="") as f:
        w=csv.DictWriter(f,fieldnames=rows[0].keys(),delimiter="\t")
        w.writeheader(); w.writerows(rows)
    print(f"rows: {len(rows)}")
    print(f"decisions_applied: {applied}")
    print(f"output: {out}")

if __name__=="__main__": main()

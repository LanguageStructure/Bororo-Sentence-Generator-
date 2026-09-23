#!/usr/bin/env python3
"""Summarize the reviewed direct-condition audit without collapsing dimensions."""
import argparse,csv,json
from collections import Counter
from pathlib import Path

FIELDS=[
 "morphological_violation","construction_mismatch",
 "s_person_mismatch","a_person_mismatch","o_person_mismatch","frame_violation",
 "constructional_overgeneralization","complementary_distribution_violation",
 "unsupported_but_plausible",
]

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument("audit")
    ap.add_argument("--output")
    a=ap.parse_args()
    with Path(a.audit).open(encoding="utf8",newline="") as f:
        rows=list(csv.DictReader(f,delimiter="\t"))
    summary={
      "rows":len(rows),
      "auditor_status":dict(Counter(r["auditor_status"] for r in rows)),
      "exact_match":dict(Counter(r["exact_match"] for r in rows)),
      "dimensions":{},
    }
    for field in FIELDS:
        c=Counter(r[field] for r in rows)
        applicable=sum(v for k,v in c.items() if k!="not_applicable")
        resolved=sum(v for k,v in c.items() if k in {"yes","no"})
        summary["dimensions"][field]={
          "counts":dict(c),
          "applicable":applicable,
          "resolved":resolved,
          "unresolved":c.get("unresolved",0),
          "yes_among_resolved":c.get("yes",0),
          "no_among_resolved":c.get("no",0),
        }
    print(f"rows: {summary['rows']}")
    print("auditor_status:",summary["auditor_status"])
    print("exact_match:",summary["exact_match"])
    for field,d in summary["dimensions"].items():
        print(f"{field}: {d['counts']}")
    if a.output:
        out=Path(a.output); out.parent.mkdir(parents=True,exist_ok=True)
        out.write_text(json.dumps(summary,ensure_ascii=False,indent=2)+"\n",encoding="utf8")
        print(f"output: {out}")

if __name__=="__main__": main()

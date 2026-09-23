#!/usr/bin/env python3
import argparse,csv,json
from pathlib import Path

FIELDS=["task_id","surface","segmentation","morphological_violation","frame_violation",
"constructional_overgeneralization","complementary_distribution_violation",
"unsupported_but_plausible","auditor_status","notes"]

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument("collected_jsonl")
    ap.add_argument("--output",required=True)
    a=ap.parse_args()
    rows=[json.loads(x) for x in Path(a.collected_jsonl).read_text(encoding="utf8").splitlines() if x.strip()]
    out=Path(a.output); out.parent.mkdir(parents=True,exist_ok=True)
    with out.open("w",encoding="utf8",newline="") as fh:
        w=csv.DictWriter(fh,fieldnames=FIELDS,delimiter="\t"); w.writeheader()
        for row in rows:
            response=row["response"]
            surface=response.get("surface","")
            w.writerow({"task_id":row["task"]["task_id"],"surface":surface,
              "segmentation":"","morphological_violation":"unresolved",
              "frame_violation":"unresolved","constructional_overgeneralization":"unresolved",
              "complementary_distribution_violation":"unresolved",
              "unsupported_but_plausible":"unresolved","auditor_status":"pending","notes":""})
    print(f"audit_rows: {len(rows)}")
    print(f"output: {out}")

if __name__=="__main__": main()

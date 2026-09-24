#!/usr/bin/env python3
"""Validate registered external-v2 extraction outputs without reading gold."""
import argparse,json
from pathlib import Path

KEYS={"item_id","observations","abstain","abstention_reason"}
OBS={"span","lemma","construction","s_person","a_person","o_person","oblique_phrase","confidence","evidence"}

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument("path",nargs="?",default="reports/external-v2/extraction-outputs.jsonl")
    a=ap.parse_args()
    rows=[json.loads(x) for x in Path(a.path).read_text(encoding="utf8").splitlines() if x.strip()]
    errors=[]
    ids=[]
    for n,r in enumerate(rows,1):
        p=r.get("parsed")
        if not isinstance(p,dict):
            errors.append(f"row {n}: unparsed response"); continue
        ids.append(p.get("item_id"))
        if set(p)!=KEYS: errors.append(f"row {n}: top-level keys {sorted(set(p)^KEYS)}")
        if not isinstance(p.get("observations"),list): errors.append(f"row {n}: observations is not a list"); continue
        if not isinstance(p.get("abstain"),bool): errors.append(f"row {n}: abstain is not boolean")
        for j,o in enumerate(p["observations"],1):
            if not isinstance(o,dict) or set(o)!=OBS:
                errors.append(f"row {n} observation {j}: invalid schema")
            elif o.get("confidence") not in {"high","medium","low"}:
                errors.append(f"row {n} observation {j}: invalid confidence")
    if len(rows)!=32: errors.append(f"expected 32 rows, found {len(rows)}")
    if len(set(ids))!=len(ids): errors.append("duplicate parsed item_id")
    if errors:
        print("\n".join(errors)); raise SystemExit(1)
    print(f"valid registered extraction: {len(rows)} rows")

if __name__=="__main__": main()

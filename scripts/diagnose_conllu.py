#!/usr/bin/env python3
import argparse,json
from pathlib import Path
from bororo_generator.diagnostics import diagnose

def main():
    p=argparse.ArgumentParser(description="Diagnose structural segmentation of a CorBo CoNLL-U file.")
    p.add_argument("conllu")
    p.add_argument("-o","--output",default="data/corbo/diagnostics.json")
    p.add_argument("--long-threshold",type=int,default=200)
    a=p.parse_args()
    d=diagnose(a.conllu,a.long_threshold)
    out=Path(a.output);out.parent.mkdir(parents=True,exist_ok=True)
    out.write_text(json.dumps(d,ensure_ascii=False,indent=2),encoding="utf-8")
    s=d["summary"]
    print(f"Units: {s.get('units',0)} | tokens: {s.get('tokens',0)} | max/unit: {s.get('max_tokens_in_unit',0)}")
    print(f"Root count != 1: {s.get('units_root_count_not_1',0)} | long units: {s.get('long_units',0)} | duplicate IDs: {s.get('units_duplicate_token_ids',0)}")
    print("Suspicious units:")
    for u in d["units"]:
        if u["roots"]!=1 or u["suspicious_long_unit"] or u["duplicate_token_ids"]:
            print(f"  {u['sent_id']}: tokens={u['tokens']} roots={u['roots']} first={u['first_token']!r} last={u['last_token']!r}")

if __name__=="__main__":main()

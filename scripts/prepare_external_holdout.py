#!/usr/bin/env python3
"""Prepare external holdout inputs without consulting grammar-v1.

This script copies only frozen documentary fields into model inputs. It does
not import bororo_generator and does not inspect grammar/configuration files.
"""
import argparse,csv,json,hashlib
from pathlib import Path

def sha(s): return hashlib.sha256(s.encode("utf8")).hexdigest()

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument("--source",default="article/external-evaluation/boe_ero_holdout_source.tsv")
    ap.add_argument("--prompt",default="article/prompts/external-extraction-v2.txt")
    ap.add_argument("--output",default="reports/external-v2/extraction-inputs.jsonl")
    ap.add_argument("--manifest",default="reports/external-v2/manifest.json")
    a=ap.parse_args()
    prompt=Path(a.prompt).read_text(encoding="utf8")
    with Path(a.source).open(encoding="utf8",newline="") as fh:
        rows=list(csv.DictReader(fh,delimiter="\t"))
    out=Path(a.output); out.parent.mkdir(parents=True,exist_ok=True)
    with out.open("w",encoding="utf8") as fh:
        for r in rows:
            task={
              "item_id":r["sample_id"],
              "documentary_id":r["documentary_id"],
              "section":int(r["section"]),
              "source":r["source"],
              "reviewed":r["reviewed"] or None,
              "portuguese":r["portuguese"],
            }
            fh.write(json.dumps({"condition":"external_extraction","task":task,"prompt":prompt},ensure_ascii=False)+"\n")
    manifest={
      "experiment_version":"external-v2",
      "items":len(rows),
      "prompt_sha256":sha(prompt),
      "source_sha256":sha(Path(a.source).read_text(encoding="utf8")),
      "grammar_access_during_preparation":False,
      "note":"Inputs contain documentary fields only; no gold labels or grammar-v1 licenses."
    }
    m=Path(a.manifest); m.parent.mkdir(parents=True,exist_ok=True)
    m.write_text(json.dumps(manifest,indent=2,ensure_ascii=False)+"\n",encoding="utf8")
    print(json.dumps(manifest,indent=2))

if __name__=="__main__": main()

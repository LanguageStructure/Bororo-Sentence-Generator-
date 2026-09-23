#!/usr/bin/env python3
"""Validate and normalize raw runner records against the frozen input inventory."""
import argparse,json
from pathlib import Path

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument("inputs")
    ap.add_argument("responses")
    ap.add_argument("--output",required=True)
    a=ap.parse_args()
    inputs=[json.loads(x) for x in Path(a.inputs).read_text(encoding="utf8").splitlines() if x.strip()]
    responses=[json.loads(x) for x in Path(a.responses).read_text(encoding="utf8").splitlines() if x.strip()]
    by_id={r["task_id"]:r for r in responses}
    if len(by_id)!=len(responses): raise SystemExit("duplicate task_id in responses")
    rows=[]
    expected_ids={x["task"]["task_id"] for x in inputs}
    for inp in inputs:
        tid=inp["task"]["task_id"]
        if tid not in by_id: raise SystemExit(f"missing response: {tid}")
        raw=by_id[tid]
        if raw.get("condition")!=inp["condition"]:
            raise SystemExit(f"condition mismatch for {tid}")
        parsed=raw.get("parsed")
        if not isinstance(parsed,dict):
            raise SystemExit(f"unparsed response: {tid}")
        if parsed.get("task_id")!=tid:
            raise SystemExit(f"parsed task_id mismatch for {tid}")
        rows.append({
          "condition":inp["condition"],
          "task":inp["task"],
          "response":parsed,
          "run_metadata":{
            "requested_model":raw.get("requested_model"),
            "returned_model":raw.get("returned_model"),
            "reasoning_effort":raw.get("reasoning_effort"),
            "executed_at_utc":raw.get("executed_at_utc"),
            "prompt_sha256":raw.get("prompt_sha256"),
            "response_id":raw.get("response_id"),
            "raw_text":raw.get("raw_text"),
          },
        })
    extra=sorted(set(by_id)-expected_ids)
    if extra: raise SystemExit(f"unexpected response task_ids: {extra}")
    p=Path(a.output); p.parent.mkdir(parents=True,exist_ok=True)
    with p.open("w",encoding="utf8") as fh:
        for row in rows: fh.write(json.dumps(row,ensure_ascii=False)+"\n")
    print(f"collected: {len(rows)}")
    print(f"output: {p}")

if __name__=="__main__": main()

#!/usr/bin/env python3
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
    for inp in inputs:
        tid=inp["task"]["task_id"]
        if tid not in by_id: raise SystemExit(f"missing response: {tid}")
        rows.append({"condition":inp["condition"],"task":inp["task"],"response":by_id[tid]})
    extra=sorted(set(by_id)-{x["task"]["task_id"] for x in inputs})
    if extra: raise SystemExit(f"unexpected response task_ids: {extra}")
    p=Path(a.output); p.parent.mkdir(parents=True,exist_ok=True)
    with p.open("w",encoding="utf8") as fh:
        for row in rows: fh.write(json.dumps(row,ensure_ascii=False)+"\n")
    print(f"collected: {len(rows)}")
    print(f"output: {p}")

if __name__=="__main__": main()

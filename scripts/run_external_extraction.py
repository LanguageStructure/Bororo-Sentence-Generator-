#!/usr/bin/env python3
"""Run the frozen external-v2 extraction experiment.

Requires OPENAI_API_KEY and the openai Python package. The runner consumes the
already frozen JSONL inputs and writes append-safe raw records. It never reads
gold annotations or grammar-v1.
"""
import argparse,hashlib,json,os
from datetime import datetime,timezone
from pathlib import Path

MODEL="gpt-5.6-sol"
REASONING_EFFORT="none"

def sha(s): return hashlib.sha256(s.encode("utf8")).hexdigest()

def parse_json(text):
    try: return json.loads(text)
    except Exception: return None

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument("--inputs",default="reports/external-v2/extraction-inputs.jsonl")
    ap.add_argument("--output",default="reports/external-v2/extraction-outputs.jsonl")
    ap.add_argument("--limit",type=int)
    a=ap.parse_args()
    if not os.environ.get("OPENAI_API_KEY"):
        raise SystemExit("OPENAI_API_KEY is not set")
    try:
        from openai import OpenAI
    except ImportError:
        raise SystemExit("Install the openai package first: python3 -m pip install openai")

    rows=[json.loads(x) for x in Path(a.inputs).read_text(encoding="utf8").splitlines() if x.strip()]
    if a.limit is not None: rows=rows[:a.limit]
    out=Path(a.output); out.parent.mkdir(parents=True,exist_ok=True)

    # Refuse accidental overwrite: the registered run is immutable.
    if out.exists() and out.stat().st_size:
        raise SystemExit(f"Refusing to overwrite existing registered output: {out}")

    client=OpenAI()
    with out.open("w",encoding="utf8") as fh:
        for row in rows:
            task=row["task"]; prompt=row["prompt"]
            user=json.dumps(task,ensure_ascii=False,separators=(",",":"))
            started=datetime.now(timezone.utc).isoformat()
            r=client.responses.create(
                model=MODEL,
                reasoning={"effort":REASONING_EFFORT},
                instructions=prompt,
                input=user,
            )
            raw=r.output_text
            rec={
              "item_id":task["item_id"],
              "documentary_id":task["documentary_id"],
              "condition":"external_extraction",
              "requested_model":MODEL,
              "returned_model":getattr(r,"model",None),
              "reasoning_effort":REASONING_EFFORT,
              "executed_at_utc":started,
              "prompt_sha256":sha(prompt),
              "input_sha256":sha(user),
              "raw_text":raw,
              "parsed":parse_json(raw),
              "response_id":getattr(r,"id",None),
            }
            fh.write(json.dumps(rec,ensure_ascii=False)+"\n")
            fh.flush()
            print(task["item_id"],"ok" if rec["parsed"] is not None else "UNPARSED")

    print(f"registered outputs: {out}")

if __name__=="__main__":
    main()

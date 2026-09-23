#!/usr/bin/env python3
"""Run one frozen experiment condition through the OpenAI Responses API.

Requires OPENAI_API_KEY and the openai Python package. Raw responses are kept.
No corpus, private dictionary, or grammar file is transmitted: only the frozen
prompt and one experimental task are sent for each request.
"""
import argparse,json,os,hashlib
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
    ap.add_argument("inputs")
    ap.add_argument("--output",required=True)
    ap.add_argument("--limit",type=int)
    a=ap.parse_args()
    if not os.environ.get("OPENAI_API_KEY"): raise SystemExit("OPENAI_API_KEY is not set")
    try:
        from openai import OpenAI
    except ImportError:
        raise SystemExit("Install the openai package first: python3 -m pip install openai")
    rows=[json.loads(x) for x in Path(a.inputs).read_text(encoding="utf8").splitlines() if x.strip()]
    if a.limit is not None: rows=rows[:a.limit]
    client=OpenAI()
    out=Path(a.output); out.parent.mkdir(parents=True,exist_ok=True)
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
            text=r.output_text
            rec={
              "task_id":task["task_id"],
              "condition":row["condition"],
              "requested_model":MODEL,
              "returned_model":getattr(r,"model",None),
              "reasoning_effort":REASONING_EFFORT,
              "executed_at_utc":started,
              "prompt_sha256":sha(prompt),
              "task":task,
              "raw_text":text,
              "parsed":parse_json(text),
              "response_id":getattr(r,"id",None),
            }
            fh.write(json.dumps(rec,ensure_ascii=False)+"\n"); fh.flush()
            print(task["task_id"],"ok" if rec["parsed"] is not None else "unparsed")
    print(f"output: {out}")

if __name__=="__main__": main()

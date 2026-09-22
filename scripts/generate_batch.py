#!/usr/bin/env python3
import argparse,json
from pathlib import Path
from bororo_generator.batch import generate_batch,batch_summary

def main():
    p=argparse.ArgumentParser(description="Generate a controlled Bororo review batch")
    p.add_argument("requests",help="JSON file containing a list of generation requests")
    p.add_argument("--output")
    a=p.parse_args()
    req=json.loads(Path(a.requests).read_text(encoding="utf-8"))
    records=generate_batch(req)
    result={"summary":batch_summary(records),"records":records}
    text=json.dumps(result,ensure_ascii=False,indent=2)
    if a.output: Path(a.output).write_text(text+"\n",encoding="utf-8")
    else: print(text)
if __name__=="__main__": main()

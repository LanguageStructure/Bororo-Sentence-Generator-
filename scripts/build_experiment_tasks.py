#!/usr/bin/env python3
"""Build the frozen v1 task inventory before any LLM outputs are collected."""
import argparse,json
from pathlib import Path
from bororo_generator.paradigm_generation import paradigm_requests
from bororo_generator.valency_review import reviewed_frame

TARGET_LEMMAS=("nudu","meru","kodu","mako","maku")

def task_from_request(i,lemma,req):
    return {
      "task_id":f"v1-{i:03d}",
      "lemma":lemma,
      "frame":reviewed_frame(lemma),
      "construction":"indicative",
      "s_person":req.get("s_person"),
      "a_person":req.get("a_person"),
      "o_person":req.get("o_person"),
      "oblique_phrase":req.get("oblique_phrase"),
    }

def build():
    out=[]; i=1
    for lemma in TARGET_LEMMAS:
        for req in paradigm_requests(lemma):
            out.append(task_from_request(i,lemma,req)); i+=1
    return out

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument("--output",required=True)
    args=ap.parse_args()
    tasks=build()
    p=Path(args.output); p.parent.mkdir(parents=True,exist_ok=True)
    with p.open("w",encoding="utf8") as fh:
        for row in tasks: fh.write(json.dumps(row,ensure_ascii=False)+"\n")
    print(f"tasks: {len(tasks)}")
    print(f"output: {p}")

if __name__=="__main__": main()

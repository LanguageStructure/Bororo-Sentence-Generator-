#!/usr/bin/env python3
"""Print a compact audit of generated cells whose predicate FORM occurs in CorBo."""
import argparse,json
from pathlib import Path
from bororo_generator.evaluation import evaluate_lexemes

def main():
    p=argparse.ArgumentParser()
    p.add_argument("corpus")
    p.add_argument("lemmas",nargs="+")
    p.add_argument("--json")
    a=p.parse_args()
    ev=evaluate_lexemes(a.lemmas,a.corpus)
    rows=[]; seen=set()
    for result in ev["results"]:
        for r in result["records"]:
            att=r.get("attestation",{})
            if not att.get("predicate_form_attested"): continue
            key=(result["lemma"],att.get("predicate_form"))
            if key in seen: continue
            seen.add(key)
            req=r.get("request",{})
            rows.append({
                "lemma":result["lemma"],
                "frame":r.get("evidence",{}).get("reviewed_frame"),
                "S":req.get("s_person"),
                "A":req.get("a_person"),
                "O":req.get("o_person"),
                "generated":r.get("text"),
                "predicate_form":att.get("predicate_form"),
                "sent_ids":list(dict.fromkeys(att.get("predicate_source_sent_ids",[]))),
            })
    if a.json:
        Path(a.json).write_text(json.dumps(rows,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
    for x in rows:
        roles=" ".join(f"{k}={x[k]}" for k in ("S","A","O") if x[k])
        print(f'{x["lemma"]}\t{x["frame"]}\t{roles}\t{x["predicate_form"]}\t{",".join(x["sent_ids"])}')
    print(f"\nTOTAL\t{len(rows)}")
if __name__=="__main__": main()

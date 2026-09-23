#!/usr/bin/env python3
"""Print a compact audit of generated predicate forms attested in CorBo.

A single surface form may correspond to more than one generated review cell.
Those possible cells are grouped instead of being collapsed to the first match.
"""
import argparse,json
from pathlib import Path
from bororo_generator.evaluation import evaluate_lexemes

def _role_signature(frame,req):
    if frame=="divalent":
        return {"A":"UNRESOLVED","O":req.get("o_person")}
    return {"S":req.get("s_person"),"A":req.get("a_person"),"O":req.get("o_person")}

def main():
    p=argparse.ArgumentParser()
    p.add_argument("corpus")
    p.add_argument("lemmas",nargs="+")
    p.add_argument("--json")
    a=p.parse_args()
    ev=evaluate_lexemes(a.lemmas,a.corpus)
    grouped={}
    for result in ev["results"]:
        for form in result.get("attested_predicate_forms",[]):
            key=(result["lemma"],form["form"])
            row=grouped.setdefault(key,{
                "lemma":result["lemma"],"frame":result.get("frame"),
                "predicate_form":form["form"],"sent_ids":set(),"possible_cells":[]
            })
            row["sent_ids"].update(form.get("sent_ids",[]))
            for req in form.get("requests",[]):
                sig=_role_signature(result.get("frame"),req)
                if sig not in row["possible_cells"]: row["possible_cells"].append(sig)
    rows=[]
    for row in grouped.values():
        row=dict(row); row["sent_ids"]=sorted(row["sent_ids"]); rows.append(row)
    if a.json:
        Path(a.json).write_text(json.dumps(rows,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
    for x in rows:
        cells=[]
        for cell in x["possible_cells"]:
            roles=" ".join(f"{k}={v}" for k,v in cell.items() if v is not None)
            if roles not in cells: cells.append(roles)
        print(f'{x["lemma"]}\t{x["frame"]}\t{" | ".join(cells)}\t{x["predicate_form"]}\t{",".join(x["sent_ids"])}')
    print(f"\nTOTAL\t{len(rows)}")
if __name__=="__main__": main()

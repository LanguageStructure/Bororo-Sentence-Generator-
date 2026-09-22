#!/usr/bin/env python3
"""Export a review packet for the lemma ako without proposing analyses."""
import argparse,json
from collections import Counter,defaultdict
from pathlib import Path
from bororo_generator.corpus import read_conllu
from bororo_generator.readiness import assess_sentence

def main():
    p=argparse.ArgumentParser();p.add_argument("conllu");p.add_argument("-o","--output",default="data/review/ako.json")
    a=p.parse_args(); rows=defaultdict(list)
    for s in read_conllu(a.conllu):
        if not assess_sentence(s)["trusted"]:continue
        ints={t["id"]:t for t in s.tokens if isinstance(t.get("id"),int)}
        for t in ints.values():
            if str(t.get("lemma") or "_")!="ako":continue
            h=ints.get(t.get("head"))
            rows[str(t.get("form") or "_")].append({
              "sent_id":s.sent_id,"text":s.text,"token_id":t["id"],
              "upos":str(t.get("upos") or "_").strip().upper(),
              "feats":t.get("feats"),"deprel":t.get("deprel"),"head":t.get("head"),
              "head_form":h.get("form") if h else None,"head_lemma":h.get("lemma") if h else None,
              "dependents":[{"id":d["id"],"form":d.get("form"),"lemma":d.get("lemma"),
                 "upos":str(d.get("upos") or "_").strip().upper(),"deprel":d.get("deprel")}
                 for d in ints.values() if d.get("head")==t["id"]]})
    out={"lemma":"ako","status":"review_required",
         "warning":"Distributional evidence only. No morphological analysis is inferred.",
         "forms":{}}
    for form,items in sorted(rows.items(),key=lambda x:(-len(x[1]),x[0])):
        out["forms"][form]={"count":len(items),
          "deprel":dict(Counter(str(x["deprel"]) for x in items)),
          "upos":dict(Counter(x["upos"] for x in items)),
          "examples":items}
    pth=Path(a.output);pth.parent.mkdir(parents=True,exist_ok=True)
    pth.write_text(json.dumps(out,ensure_ascii=False,indent=2),encoding="utf-8")
    print(f"ako tokens: {sum(len(x) for x in rows.values())} | forms: {len(rows)} | {pth}")
    for f,x in out["forms"].items():print(f"  {f}: {x['count']} | DEPREL={x['deprel']}")

if __name__=="__main__":main()

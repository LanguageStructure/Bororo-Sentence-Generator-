#!/usr/bin/env python3
import argparse,json
from pathlib import Path
from bororo_generator.corpus import read_conllu
from bororo_generator.readiness import assess_sentence
from bororo_generator.templates import from_sentence

def main():
    p=argparse.ArgumentParser(description="Export trusted attested structures as evidence templates.")
    p.add_argument("conllu");p.add_argument("-o","--output",default="data/corbo/attested-templates.json")
    a=p.parse_args();all_s=list(read_conllu(a.conllu))
    trusted=[s for s in all_s if assess_sentence(s)["trusted"]]
    data={"source":a.conllu,"parsed_units":len(all_s),"trusted_units":len(trusted),
          "note":"Descriptive evidence only; templates are not generation rules.",
          "templates":[from_sentence(s).to_dict() for s in trusted]}
    out=Path(a.output);out.parent.mkdir(parents=True,exist_ok=True)
    out.write_text(json.dumps(data,ensure_ascii=False,indent=2),encoding="utf-8")
    print(f"Parsed: {len(all_s)} | trusted: {len(trusted)} | exported: {out}")

if __name__=="__main__":main()

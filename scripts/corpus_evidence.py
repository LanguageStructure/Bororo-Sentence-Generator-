#!/usr/bin/env python3
import argparse,json
from pathlib import Path
from bororo_generator.corpus_evidence import corpus_lexeme_inventory

def main():
    p=argparse.ArgumentParser(description="Report corpus-only lemma/form observations without licensing generation")
    p.add_argument("corpus")
    p.add_argument("lemmas",nargs="+")
    p.add_argument("--output",required=True)
    a=p.parse_args()
    report=corpus_lexeme_inventory(a.lemmas,a.corpus)
    out=Path(a.output); out.parent.mkdir(parents=True,exist_ok=True)
    out.write_text(json.dumps(report,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
    print("report:",out)
    for row in report["lexemes"]:
        print(row["lemma"],"forms:",len(row["forms"]),"tokens:",sum(x["count"] for x in row["forms"]))
if __name__=="__main__": main()

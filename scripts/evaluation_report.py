#!/usr/bin/env python3
import argparse,json
from pathlib import Path
from bororo_generator.evaluation_report import evaluation_report

def main():
    p=argparse.ArgumentParser(description="Write a reproducible controlled-generation evaluation report")
    p.add_argument("corpus")
    p.add_argument("lemmas",nargs="+")
    p.add_argument("--output",required=True)
    a=p.parse_args()
    report=evaluation_report(a.lemmas,a.corpus)
    Path(a.output).write_text(json.dumps(report,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
    s=report["summary"]
    print("report:",a.output)
    print("lexemes:",s["lexemes"])
    print("generated_records:",s["generated_records"])
    print("unique_predicate_forms_attested:",s["unique_predicate_forms_attested"])
if __name__=="__main__": main()

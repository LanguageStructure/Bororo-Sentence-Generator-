#!/usr/bin/env python3
import argparse,json
from bororo_generator.evaluation import evaluate_lexemes

def main():
    p=argparse.ArgumentParser(description="Evaluate reviewed generated paradigms against CorBo")
    p.add_argument("corpus")
    p.add_argument("lemmas",nargs="+")
    p.add_argument("--output")
    a=p.parse_args()
    result=evaluate_lexemes(a.lemmas,a.corpus)
    out=json.dumps(result,ensure_ascii=False,indent=2)
    if a.output:
        from pathlib import Path
        Path(a.output).write_text(out+"\n",encoding="utf-8")
    else: print(out)
if __name__=="__main__": main()

#!/usr/bin/env python3
import argparse,json
from pathlib import Path
from bororo_generator.corpus import corpus_summary
from bororo_generator.report import build_report
from bororo_generator.readiness import assess_corpus

def main():
    p=argparse.ArgumentParser(description="Build conservative evidence from an evolving CorBo CoNLL-U file.")
    p.add_argument("conllu")
    p.add_argument("-o","--output",default="data/corbo/evidence.json")
    p.add_argument("--trusted-output",default="data/corbo/trusted-evidence.json")
    p.add_argument("--readiness-output",default="data/corbo/readiness.json")
    p.add_argument("--max-tokens",type=int,default=100)
    p.add_argument("--top",type=int,default=100)
    a=p.parse_args()

    summary=corpus_summary(a.conllu)
    trusted,excluded=assess_corpus(a.conllu,a.max_tokens)
    readiness={
      "source":str(a.conllu),"policy":{"max_tokens":a.max_tokens},
      "summary":{"parsed_units":len(trusted)+len(excluded),
                 "trusted_units":len(trusted),"excluded_units":len(excluded),
                 "trusted_tokens":sum(len(s.tokens) for s,_ in trusted),
                 "excluded_tokens":sum(len(s.tokens) for s,_ in excluded)},
      "excluded":[x for _,x in excluded]
    }
    ro=Path(a.readiness_output);ro.parent.mkdir(parents=True,exist_ok=True)
    ro.write_text(json.dumps(readiness,ensure_ascii=False,indent=2),encoding="utf-8")

    # Full evidence remains diagnostic only.
    report=build_report(a.conllu,top=a.top)
    eo=Path(a.output);eo.parent.mkdir(parents=True,exist_ok=True)
    eo.write_text(json.dumps(report,ensure_ascii=False,indent=2),encoding="utf-8")

    # Trusted evidence is intentionally metadata-only until a filtered CoNLL-U
    # serializer is introduced; this prevents accidental use of excluded blocks.
    trusted_report={"source":str(a.conllu),"status":"trusted_only",
      "policy":{"max_tokens":a.max_tokens},
      "summary":readiness["summary"],
      "sentences":[{"sent_id":x.sent_id,"text":x.text,"tokens":len(x.tokens)} for x,_ in trusted]}
    to=Path(a.trusted_output);to.parent.mkdir(parents=True,exist_ok=True)
    to.write_text(json.dumps(trusted_report,ensure_ascii=False,indent=2),encoding="utf-8")

    print(f"CorBo parsed: {summary['sentences']} units, {summary['tokens']} tokens")
    print(f"Trusted: {len(trusted)} units / {readiness['summary']['trusted_tokens']} tokens")
    print(f"Excluded: {len(excluded)} units / {readiness['summary']['excluded_tokens']} tokens")
    print(f"Wrote {eo}, {to}, {ro}")

if __name__=="__main__": main()

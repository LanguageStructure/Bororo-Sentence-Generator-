#!/usr/bin/env python3
import argparse,json
from bororo_generator.corpus import read_conllu
from bororo_generator.readiness import assess_sentence
from bororo_generator.recombine import recombine,compatible

def main():
    p=argparse.ArgumentParser(description="Find one conservative recombination in trusted UD sentences.")
    p.add_argument("conllu");p.add_argument("--max-tokens",type=int,default=100)
    a=p.parse_args()
    sentences=[s for s in read_conllu(a.conllu) if assess_sentence(s,a.max_tokens)["trusted"]]
    for target in sentences:
        for donor in sentences:
            if target.sent_id==donor.sent_id: continue
            for t in target.tokens:
                for d in donor.tokens:
                    if compatible(t,d) and t.get("form")!=d.get("form"):
                        print(json.dumps(recombine(target,donor,t["id"],d["id"]).record(),
                                         ensure_ascii=False,indent=2))
                        return
    print("No licensed recombination found in trusted evidence.")

if __name__=="__main__":main()

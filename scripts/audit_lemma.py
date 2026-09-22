#!/usr/bin/env python3
import argparse
from collections import Counter
from bororo_generator.corpus import read_conllu
from bororo_generator.readiness import assess_sentence
from bororo_generator.slots import lemma_realizations

def main():
    p=argparse.ArgumentParser(description="Audit surface realizations and syntactic environments of a lemma.")
    p.add_argument("conllu");p.add_argument("lemma");p.add_argument("--examples",type=int,default=5)
    a=p.parse_args()
    ss=[s for s in read_conllu(a.conllu) if assess_sentence(s)["trusted"]]
    byid={s.sent_id:s for s in ss}; data=lemma_realizations(ss).get(a.lemma,{})
    print(f"Lemma: {a.lemma} | forms: {len(data)} | tokens: {sum(map(len,data.values()))}")
    for form,slots in sorted(data.items(),key=lambda kv:(-len(kv[1]),kv[0])):
        env=Counter((x.upos,x.deprel,x.head_lemma,x.head_upos) for x in slots)
        print(f"\n{form}: {len(slots)}")
        for (upos,dep,hl,hu),n in env.most_common():
            print(f"  {n} × UPOS={upos} DEPREL={dep} HEAD={hl}/{hu}")
        seen=set()
        for x in slots:
            if x.sent_id not in seen:
                print(f"    [{x.sent_id}] {byid[x.sent_id].text}");seen.add(x.sent_id)
                if len(seen)>=a.examples:break

if __name__=="__main__":main()

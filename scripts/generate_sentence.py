#!/usr/bin/env python3
import argparse,json
from bororo_generator.api import generate_record

def main():
    p=argparse.ArgumentParser(description="Controlled Bororo declarative generator")
    p.add_argument("lemma")
    p.add_argument("--s")
    p.add_argument("--a")
    p.add_argument("--o")
    p.add_argument("--oblique")
    p.add_argument("--overt-a")
    p.add_argument("--overt-o")
    args=p.parse_args()
    result=generate_record(
        args.lemma,s_person=args.s,a_person=args.a,o_person=args.o,
        oblique_phrase=args.oblique,overt_a=args.overt_a,overt_o=args.overt_o
    )
    print(json.dumps(result,ensure_ascii=False,indent=2))
if __name__=="__main__": main()

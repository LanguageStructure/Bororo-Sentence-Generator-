#!/usr/bin/env python3
import argparse
from bororo_generator.report import build_report
def main():
 p=argparse.ArgumentParser();p.add_argument("conllu");p.add_argument("-o","--output",default="data/corbo/evidence.json");p.add_argument("--top",type=int,default=100);a=p.parse_args()
 d=build_report(a.conllu,a.output,a.top);s=d["summary"]
 print(f"CorBo: {s['sentences']} sentences, {s['tokens']} tokens, {s['types']} forms, {s['lemmas']} lemmas")
 print(f"Wrote {a.output}")
if __name__=="__main__":main()

#!/usr/bin/env python3
import argparse,json
from bororo_generator.paradigm_generation import generate_paradigm
from bororo_generator.batch import batch_summary
from bororo_generator.attestation import surface_attestation
from bororo_generator.corpus import read_conllu

def main():
    p=argparse.ArgumentParser(description="Generate all currently licensed cells for a reviewed Bororo lexeme")
    p.add_argument("lemma")
    p.add_argument("--corpus")
    a=p.parse_args()
    idx=surface_attestation(read_conllu(a.corpus)) if a.corpus else None
    records=generate_paradigm(a.lemma,idx)
    print(json.dumps({"lemma":a.lemma,"summary":batch_summary(records),"records":records},
                     ensure_ascii=False,indent=2))
if __name__=="__main__": main()

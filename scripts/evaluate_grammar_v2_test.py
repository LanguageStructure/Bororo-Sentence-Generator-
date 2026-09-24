#!/usr/bin/env python3
"""Evaluate the frozen grammar-v2 on the sealed source-group test partition.

Run only after config/valency_review_v2_frozen.yaml has been frozen.
This script mechanically extracts test predicate occurrences and compares their
annotated dependency evidence with the frozen lexical licenses. It never edits
the grammar and reports coverage separately from evaluable licensed cases.
"""
from __future__ import annotations
import json, re, sys
from collections import Counter, defaultdict
from pathlib import Path
import yaml

TEST_GROUPS={"ABE","BEBE","C.O"}
EXCLUDED_IDS={"OBE-p75.1","OBE-p75.2","00FFW.001-antonioWWA.1","00CrowellThesis-sent71"}
CORE_OBJ={"obj","iobj"}

def group(sent_id):
    for g in TEST_GROUPS:
        if g in sent_id: return g
    return None

def read_conllu(path):
    sent=[]; meta={}
    for line in Path(path).read_text(encoding="utf8").splitlines()+[""]:
        if line.startswith("# sent_id = "): meta["sent_id"]=line.split("=",1)[1].strip()
        elif line.startswith("# text = "): meta["text"]=line.split("=",1)[1].strip()
        elif line and not line.startswith("#"):
            cols=line.split("\t")
            if len(cols)>=8 and "-" not in cols[0] and "." not in cols[0]:
                sent.append(cols)
        elif not line and sent:
            yield meta,sent; sent=[]; meta={}

def main():
    if len(sys.argv)!=2:
        raise SystemExit("usage: evaluate_grammar_v2_test.py CORPUS.conllu")
    cfg=yaml.safe_load(Path("config/valency_review_v2_frozen.yaml").read_text())
    lex=cfg["lexemes"]
    counts=Counter(); bylemma=defaultdict(Counter); rows=[]
    for meta,toks in read_conllu(sys.argv[1]):
        sid=meta.get("sent_id","")
        g=group(sid)
        if not g or sid in EXCLUDED_IDS: continue
        counts["test_sentences"]+=1
        for t in toks:
            lemma=t[2]; upos=t[3]
            if upos not in {"VERB","AUX"}: continue
            counts["predicate_tokens"]+=1
            if lemma not in lex:
                counts["unlicensed_predicate_tokens"]+=1; continue
            counts["licensed_predicate_tokens"]+=1
            frame=lex[lemma]["frame"]
            deps=[x[7].split(":")[0] for x in toks if x[6]==t[0]]
            nobj=sum(d in CORE_OBJ for d in deps)
            outcome="not_mechanically_scorable"
            if frame=="monovalent":
                outcome="match" if nobj==0 else "frame_mismatch"
            elif frame in {"divalent","reflexive_divalent"}:
                outcome="match" if nobj>=1 else "annotation_or_implicit_object"
            elif frame in {"extended_intransitive","intransitive_with_postpositional_complement","identificational_copula"}:
                outcome="manual_required"
            counts[outcome]+=1; bylemma[lemma][outcome]+=1
            rows.append({"sent_id":sid,"group":g,"lemma":lemma,"form":t[1],"frame":frame,"dependent_relations":deps,"outcome":outcome})
    out={"freeze_config":"config/valency_review_v2_frozen.yaml","test_groups":sorted(TEST_GROUPS),"counts":dict(counts),"by_lemma":{k:dict(v) for k,v in sorted(bylemma.items())},"items":rows,
         "interpretation":"Mechanical UD comparison is diagnostic only. annotation_or_implicit_object is not an automatic grammar error (e.g. zero/omitted objects); manual_required cases must be adjudicated without changing the frozen grammar."}
    Path("reports/grammar-v2").mkdir(parents=True,exist_ok=True)
    Path("reports/grammar-v2/test-evaluation.json").write_text(json.dumps(out,ensure_ascii=False,indent=2)+"\n",encoding="utf8")
    print(json.dumps(out["counts"],ensure_ascii=False,indent=2))
if __name__=="__main__": main()

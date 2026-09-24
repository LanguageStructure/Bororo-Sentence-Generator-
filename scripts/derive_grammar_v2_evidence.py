#!/usr/bin/env python3
"""Derive auditable predicate evidence from the frozen grammar-v2 development set."""
import argparse,json,collections,hashlib
from pathlib import Path

def blocks(text):
    cur=[]
    for l in text.splitlines()+[""]:
        if l.strip(): cur.append(l)
        elif cur: yield cur; cur=[]

def meta(b,key):
    p="# "+key+" = "
    for l in b:
        if l.startswith(p): return l[len(p):]
    return ""

def feats(s):
    if not s or s=="_": return {}
    out={}
    for x in s.split("|"):
        if "=" in x:
            k,v=x.split("=",1);out[k]=v
    return out

def main():
    ap=argparse.ArgumentParser();ap.add_argument("conllu");ap.add_argument("--out",required=True);a=ap.parse_args()
    raw=Path(a.conllu).read_text(encoding="utf8")
    lemmas=collections.defaultdict(lambda:{"occurrences":0,"root_occurrences":0,"relations":collections.Counter(),"persons":collections.Counter(),"forms":collections.Counter(),"examples":[]})
    for b in blocks(raw):
        sid=meta(b,"sent_id"); text=meta(b,"text"); por=meta(b,"text_por") or meta(b,"translation_pt")
        for l in b:
            if l.startswith("#"): continue
            c=l.split("\t")
            if len(c)!=10 or "-" in c[0] or "." in c[0]: continue
            form,lemma,upos,fs,head,rel=c[1],c[2],c[3],c[5],c[6],c[7]
            if upos not in {"VERB","AUX"} or lemma in {"_",""}: continue
            d=lemmas[lemma];d["occurrences"]+=1;d["root_occurrences"]+=(rel=="root");d["relations"][rel]+=1;d["forms"][form]+=1
            f=feats(fs)
            person=f.get("Person") or f.get("Person[subj]") or f.get("Person[obj]")
            number=f.get("Number") or f.get("Number[subj]") or f.get("Number[obj]")
            if person: d["persons"][f"{person}:{number or '?'}"]+=1
            if len(d["examples"])<5:d["examples"].append({"sent_id":sid,"form":form,"relation":rel,"feats":fs,"text":text,"text_por":por})
    out=[]
    for lemma,d in sorted(lemmas.items(),key=lambda x:(-x[1]["occurrences"],x[0])):
        out.append({"lemma":lemma,"occurrences":d["occurrences"],"root_occurrences":d["root_occurrences"],"relations":dict(d["relations"]),"persons":dict(d["persons"]),"forms":dict(d["forms"].most_common()),"examples":d["examples"],"status":"corpus_evidence_only","grammar_license":False})
    payload={"source":a.conllu,"source_sha256":hashlib.sha256(raw.encode()).hexdigest(),"predicate_lemmas":len(out),"note":"Development-only corpus observations. No entry is a grammar license without linguistic review.","lemmas":out}
    Path(a.out).parent.mkdir(parents=True,exist_ok=True);Path(a.out).write_text(json.dumps(payload,ensure_ascii=False,indent=2)+"\n",encoding="utf8")
    print("predicate lemmas:",len(out));print("predicate tokens:",sum(x["occurrences"] for x in out))
if __name__=="__main__":main()

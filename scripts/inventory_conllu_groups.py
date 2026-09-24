#!/usr/bin/env python3
"""Inventory CoNLL-U source groups before a grouped train/test split.

No split is performed here. The inventory is intended to be inspected for
provenance/review status before partition membership is frozen.
"""
import argparse,collections,json,re
from pathlib import Path

def sentences(text):
    cur=[]
    for line in text.splitlines()+[""]:
        if line.strip():
            cur.append(line)
        elif cur:
            yield cur; cur=[]

def meta(block,key):
    prefix="# "+key+" = "
    for line in block:
        if line.startswith(prefix): return line[len(prefix):]
    return ""

def source_group(block):
    # sourcefile values in legacy CorBo are often sentence-level filenames
    # (e.g. 0057a.PessGr). Collapse them to documentary collections.
    raw=""
    for line in block:
        if line.startswith("# meta:"):
            m=re.search(r"(?:^|;\\s*)sourcefile=([^;]*)",line[7:].strip())
            if m: raw=m.group(1).strip()
    sid=meta(block,"sent_id")
    probe=raw or sid
    rules=[
      (r"PessGr", "PessGr"), (r"EncI?E[x]?", "EncIE"), (r"IETKB", "IETKB"),
      (r"KJB", "KJB"), (r"KoeMakarewudo", "KoeMakarewudo"),
      (r"dialogomulherAeB", "dialogomulherAeB"), (r"RaimundoItogoga", "RaimundoItogoga"),
      (r"BEBE", "BEBE"), (r"CGPB", "CGPB"), (r"KuiejedogeEiodudo", "KuiejedogeEiodudo"),
      (r"NT\\.CG", "NT.CG"), (r"NT\\.GO", "NT.GO"), (r"^RO-", "RO"),
      (r"^C\\.O\\.", "C.O"), (r"^ABE", "ABE"), (r"^criacao", "criacao"),
      (r"^sabia", "sabia"), (r"^FWFFG", "FWFFG"),
    ]
    for pat,name in rules:
        if re.search(pat,probe,re.I): return name
    return raw or sid or "UNKNOWN"

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument("conllu")
    ap.add_argument("--output",required=True)
    a=ap.parse_args()
    groups=collections.defaultdict(lambda:{"sentences":0,"sent_ids":[],"with_pt":0,"with_eng":0})
    for b in sentences(Path(a.conllu).read_text(encoding="utf8")):
        g=source_group(b); sid=meta(b,"sent_id")
        d=groups[g]; d["sentences"]+=1; d["sent_ids"].append(sid)
        d["with_pt"]+=bool(meta(b,"text_por") or meta(b,"translation_pt"))
        d["with_eng"]+=bool(meta(b,"text_eng") or meta(b,"translation_en"))
    payload={"source":a.conllu,"groups":[{"source_group":g,**d} for g,d in sorted(groups.items())]}
    Path(a.output).parent.mkdir(parents=True,exist_ok=True)
    Path(a.output).write_text(json.dumps(payload,ensure_ascii=False,indent=2)+"\n",encoding="utf8")
    print("groups:",len(groups)); print("sentences:",sum(x["sentences"] for x in groups.values()))

if __name__=="__main__": main()

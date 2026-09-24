#!/usr/bin/env python3
"""Build development-only CoNLL-U for grammar-v2.

TEST collections are hard-coded from the preregistered partition and are never
written to the development artifact.
"""
from pathlib import Path
import argparse,re,hashlib,json

TEST={"ABE","BEBE","C.O"}
EXCLUDE={"OBE-p75.1","OBE-p75.2","00FFW.001-antonioWWA.1","00CrowellThesis-sent71"}

def blocks(text):
    cur=[]
    for line in text.splitlines()+[""]:
        if line.strip(): cur.append(line)
        elif cur: yield cur; cur=[]

def sid(b):
    for l in b:
        if l.startswith("# sent_id = "): return l[12:].strip()
    return ""

def group(b):
    i=sid(b); raw=""
    for l in b:
        if l.startswith("# meta:"):
            m=re.search(r"(?:^|;\s*)sourcefile=([^;]*)",l[7:].strip())
            if m: raw=m.group(1).strip()
    p=raw or i
    rules=[(r"PessGr","PessGr"),(r"EncI?E[x]?","EncIE"),(r"IETKB","IETKB"),
    (r"KJB","KJB"),(r"KoeMakarewudo","KoeMakarewudo"),(r"dialogomulherAeB","dialogomulherAeB"),
    (r"RaimundoItogoga","RaimundoItogoga"),(r"BEBE","BEBE"),(r"CGPB","CGPB"),
    (r"KuiejedogeEiodudo","KuiejedogeEiodudo"),(r"NT\.CG","NT.CG"),(r"NT\.GO","NT.GO"),
    (r"^RO-","RO"),(r"^C\.O\.","C.O"),(r"^ABE","ABE"),(r"^criacao","criacao"),
    (r"^sabia","sabia"),(r"^FWFFG","FWFFG")]
    for pat,n in rules:
        if re.search(pat,p,re.I): return n
    return raw or i

def main():
    ap=argparse.ArgumentParser();ap.add_argument("source");ap.add_argument("--out",required=True);ap.add_argument("--manifest",required=True);a=ap.parse_args()
    raw=Path(a.source).read_text(encoding="utf8"); dev=[]; counts={}
    excluded=[]
    for b in blocks(raw):
        i=sid(b); g=group(b)
        if i in EXCLUDE: excluded.append(i); continue
        counts[g]=counts.get(g,0)+1
        if g not in TEST: dev.append(b)
    out="\n\n".join("\n".join(b) for b in dev)+"\n"
    Path(a.out).parent.mkdir(parents=True,exist_ok=True);Path(a.out).write_text(out,encoding="utf8")
    man={"source":a.source,"source_sha256":hashlib.sha256(raw.encode()).hexdigest(),"development_sentences":len(dev),"test_collections":sorted(TEST),"test_sentence_count":sum(counts.get(x,0) for x in TEST),"excluded_singletons":excluded,"development_sha256":hashlib.sha256(out.encode()).hexdigest()}
    Path(a.manifest).write_text(json.dumps(man,indent=2)+"\n",encoding="utf8")
    assert len(dev)==627, len(dev); assert man["test_sentence_count"]==157,man
    print("development: 627");print("sealed test: 157");print("excluded: 4")

if __name__=="__main__":main()

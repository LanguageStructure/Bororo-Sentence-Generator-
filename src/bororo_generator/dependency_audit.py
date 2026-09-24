"""Audit what changes around attested forms of one lemma.

Descriptive only: differences are evidence for review, not agreement rules.
"""
from collections import Counter,defaultdict

def _feats(t):
    f=t.get("feats") or {}
    return "|".join(f"{k}={f[k]}" for k in sorted(f)) if isinstance(f,dict) else str(f)

def audit_lemma_context(sentences,lemma):
    forms=defaultdict(lambda:{"count":0,"deprel":Counter(),"head":Counter(),"dependents":Counter(),"examples":[]})
    for s in sentences:
        byid={t["id"]:t for t in s.tokens if isinstance(t.get("id"),int)}
        for t in byid.values():
            if str(t.get("lemma") or "")!=lemma: continue
            key=str(t.get("form") or "").casefold()
            d=forms[key];d["count"]+=1;d["deprel"][str(t.get("deprel") or "_")]+=1
            h=byid.get(t.get("head"))
            d["head"][f"{(h or {}).get('lemma','ROOT')}:{(h or {}).get('upos','ROOT')}"]+=1
            for x in byid.values():
                if x.get("head")==t.get("id"):
                    d["dependents"][f"{x.get('deprel','_')}|{x.get('lemma','_')}|{x.get('upos','_')}|{_feats(x)}"]+=1
            if len(d["examples"])<8:d["examples"].append({"sent_id":s.sent_id,"text":s.text})
    return forms

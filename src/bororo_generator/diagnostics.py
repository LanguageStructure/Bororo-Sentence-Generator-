"""Diagnostics for evolving CorBo CoNLL-U files.

The diagnostic layer is deliberately tolerant: it reports structural problems
instead of silently treating malformed blocks as trustworthy sentences.
"""
from collections import Counter
from .corpus import read_conllu

def diagnose(path, long_threshold=200):
    units=[]; totals=Counter()
    for s in read_conllu(path):
        roots=[t for t in s.tokens if t.get("head")==0]
        ids=[t.get("id") for t in s.tokens]
        unit={
            "sent_id":s.sent_id,
            "text":s.text,
            "tokens":len(s.tokens),
            "roots":len(roots),
            "root_forms":[str(t.get("form","")) for t in roots[:10]],
            "first_token":str(s.tokens[0].get("form","")) if s.tokens else "",
            "last_token":str(s.tokens[-1].get("form","")) if s.tokens else "",
            "duplicate_token_ids":len(ids)!=len(set(ids)),
            "suspicious_long_unit":len(s.tokens)>long_threshold,
            "missing_text":not bool(s.text.strip()),
        }
        units.append(unit)
        totals["units"]+=1;totals["tokens"]+=len(s.tokens)
        if unit["roots"]!=1:totals["units_root_count_not_1"]+=1
        if unit["suspicious_long_unit"]:totals["long_units"]+=1
        if unit["duplicate_token_ids"]:totals["units_duplicate_token_ids"]+=1
        if unit["missing_text"]:totals["units_missing_text"]+=1
    totals["max_tokens_in_unit"]=max((u["tokens"] for u in units),default=0)
    return {"summary":dict(totals),"units":units}

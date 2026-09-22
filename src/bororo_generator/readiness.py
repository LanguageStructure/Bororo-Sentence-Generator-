"""Conservative readiness filtering for evolving CorBo CoNLL-U data."""
from .corpus import read_conllu

def assess_sentence(s, max_tokens=100):
    reasons=[]
    n=len(s.tokens)
    roots=[t for t in s.tokens if t.get("head")==0]
    forms=[str(t.get("form","")) for t in s.tokens]
    ids=[t.get("id") for t in s.tokens]
    if n==0: reasons.append("empty")
    if n>max_tokens: reasons.append("too_long")
    if len(roots)!=1: reasons.append("root_count_not_1")
    if len(ids)!=len(set(ids)): reasons.append("duplicate_token_ids")
    if not s.text.strip(): reasons.append("missing_text")
    if any("<w:" in f or "</w:" in f or "w:val=" in f for f in forms):
        reasons.append("xml_contamination")
    return {"trusted":not reasons,"reasons":reasons,"tokens":n,
            "sent_id":s.sent_id,"text":s.text}

def assess_corpus(path,max_tokens=100):
    trusted=[];excluded=[]
    for s in read_conllu(path):
        a=assess_sentence(s,max_tokens)
        (trusted if a["trusted"] else excluded).append((s,a))
    return trusted,excluded

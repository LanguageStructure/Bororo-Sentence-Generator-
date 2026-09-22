"""Structural readiness checks for CoNLL-U generation evidence."""
def assess_sentence(s,max_tokens=100):
    reasons=[]
    toks=[t for t in s.tokens if isinstance(t.get("id"),int)]
    ids=[t["id"] for t in toks]
    if not toks: reasons.append("empty")
    if len(toks)>max_tokens: reasons.append("too_long")
    true_roots=[t for t in toks if t.get("head")==0 and t.get("deprel")=="root"]
    if len(true_roots)!=1: reasons.append("root_count_not_1")
    # A token labelled root with a non-zero head is internally inconsistent.
    stray_roots=[t for t in toks if t.get("deprel")=="root" and t.get("head")!=0]
    if stray_roots: reasons.append("root_deprel_nonzero_head")
    if len(ids)!=len(set(ids)): reasons.append("duplicate_ids")
    if not getattr(s,"text",None): reasons.append("missing_text")
    text=getattr(s,"text","") or ""
    if any(x in text for x in ("<w:","</w:","<xml","<?xml")): reasons.append("xml_contamination")
    return {"trusted":not reasons,"reasons":reasons,"sent_id":getattr(s,"sent_id",None),
            "tokens":len(toks)}

def assess_corpus(sentences,max_tokens=100):
    results=[assess_sentence(s,max_tokens) for s in sentences]
    return {"trusted":[x for x in results if x["trusted"]],
            "excluded":[x for x in results if not x["trusted"]]}

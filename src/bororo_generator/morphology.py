"""Evidence-first morphology inventory.

No segmentation or feature value is invented here. The inventory records only
surface forms and FEATS already present in trusted CoNLL-U evidence.
"""
from collections import defaultdict,Counter
from .slots import sentence_slots

def feature_string(feats):
    if not feats:return "_"
    if isinstance(feats,dict):
        return "|".join(f"{k}={feats[k]}" for k in sorted(feats))
    return str(feats)

def morphology_inventory(sentences):
    inv=defaultdict(lambda:defaultdict(Counter))
    for s in sentences:
        byid={t["id"]:t for t in s.tokens if isinstance(t.get("id"),int)}
        for slot in sentence_slots(s):
            tok=byid[slot.token_id]
            inv[slot.lemma][slot.form][feature_string(tok.get("feats"))]+=1
    return inv

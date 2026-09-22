"""Descriptive paradigms from attested FEATS. No morpheme segmentation is inferred."""
from collections import defaultdict,Counter
from .morphology import feature_string

def descriptive_paradigm(sentences,lemma):
    cells=defaultdict(Counter)
    examples=defaultdict(list)
    for s in sentences:
        for t in s.tokens:
            if not isinstance(t.get("id"),int) or str(t.get("lemma") or "_")!=lemma:continue
            feats=feature_string(t.get("feats"))
            form=str(t.get("form") or "_").casefold()
            cells[feats][form]+=1
            if len(examples[(feats,form)])<5:
                examples[(feats,form)].append({"sent_id":s.sent_id,"text":s.text})
    return {"lemma":lemma,"cells":{f:dict(c) for f,c in cells.items()},"examples":dict(examples)}

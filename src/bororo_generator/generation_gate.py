"""Central gate preventing unreviewed morphology from entering generation."""
from dataclasses import dataclass,field
from typing import List
from .review import generation_ready,cell_generation_ready
from .valency_review import reviewed_frame
from .lexical_review import review_status

@dataclass
class GateResult:
    allowed:bool
    blocked_lemmas:List[str]=field(default_factory=list)
    reasons:List[str]=field(default_factory=list)

def check_lemmas(lemmas,review_path="config/morphology_review.yaml"):
    blocked=sorted({x for x in lemmas if x and x!="_" and not generation_ready(x,review_path)})
    reasons=["human morphology review required"] if blocked else []
    return GateResult(not blocked,blocked,reasons)

def check_tokens(tokens,review_path="config/morphology_review.yaml"):
    """Gate tokens by whole-lemma approval OR exact reviewed FEATS+form cell."""
    blocked=[]
    reasons=[]
    for t in tokens:
        if not isinstance(t.get("id"),int): continue
        upos=str(t.get("upos") or "_").strip().upper()
        lemma=str(t.get("lemma") or "_")
        if upos=="PUNCT" or lemma=="_": continue
        if generation_ready(lemma,review_path): continue
        if cell_generation_ready(lemma,t.get("feats") or {},t.get("form"),review_path): continue
        label=f"{lemma}:{t.get('form') or '_'}"
        if label not in blocked: blocked.append(label)
    if blocked: reasons.append("human morphology review required for exact lemma/form/FEATS")
    return GateResult(not blocked,blocked,reasons)


def check_lexical_generation(lemmas,review_path="config/morphology_review.yaml",valency_path="config/valency_review.yaml"):
    """Require independent morphology and coding-frame evidence for lexical generation."""
    blocked=[];reasons=[]
    for lemma in sorted({x for x in lemmas if x and x!="_"}):
        missing=[]
        status=review_status(lemma,reviewed_frame(lemma,valency_path),None)
        if status=="construction_ambiguity": missing.append("construction_ambiguity")
        if not generation_ready(lemma,review_path): missing.append("morphology")
        if reviewed_frame(lemma,valency_path) is None: missing.append("coding_frame")
        if missing: blocked.append(f"{lemma}:"+",".join(missing))
    if blocked: reasons.append("independent morphology, coding-frame, and lexical-review clearance required")
    return GateResult(not blocked,blocked,reasons)

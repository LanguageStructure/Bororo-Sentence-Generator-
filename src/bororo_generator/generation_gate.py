"""Central gate preventing unreviewed morphology from entering generation."""
from dataclasses import dataclass,field
from typing import List
from .review import generation_ready

@dataclass
class GateResult:
    allowed:bool
    blocked_lemmas:List[str]=field(default_factory=list)
    reasons:List[str]=field(default_factory=list)

def check_lemmas(lemmas,review_path="config/morphology_review.yaml"):
    blocked=sorted({x for x in lemmas if x and x!="_" and not generation_ready(x,review_path)})
    reasons=[]
    if blocked:
        reasons.append("human morphology review required")
    return GateResult(not blocked,blocked,reasons)

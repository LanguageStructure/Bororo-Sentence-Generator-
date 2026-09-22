"""Human-reviewed linguistic knowledge layer."""
from pathlib import Path
import yaml

def load_review(path="config/morphology_review.yaml"):
    p=Path(path)
    if not p.exists(): return {"lemmas":{}}
    return yaml.safe_load(p.read_text(encoding="utf-8")) or {"lemmas":{}}

def lemma_review(lemma,path="config/morphology_review.yaml"):
    return load_review(path).get("lemmas",{}).get(lemma)

def generation_ready(lemma,path="config/morphology_review.yaml"):
    # Whole-lemma approval remains deliberately strict.
    x=lemma_review(lemma,path)
    return bool(x and x.get("status")=="approved")

def approved_form(lemma,feats,path="config/morphology_review.yaml"):
    """Return the reviewed surface form for an exact FEATS cell, or None."""
    x=lemma_review(lemma,path) or {}
    wanted={str(k):str(v) for k,v in (feats or {}).items()}
    for cell in x.get("approved_cells",[]) or []:
        got={str(k):str(v) for k,v in (cell.get("feats") or {}).items()}
        if got==wanted:return cell.get("form")
    return None

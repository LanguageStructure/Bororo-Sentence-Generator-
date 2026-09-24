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
    x=lemma_review(lemma,path)
    return bool(x and x.get("status")=="approved")

def _norm_feats(feats):
    return {str(k):str(v) for k,v in (feats or {}).items()}

def approved_form(lemma,feats,path="config/morphology_review.yaml"):
    """Return reviewed surface form for an exact FEATS cell, or None."""
    x=lemma_review(lemma,path) or {}
    wanted=_norm_feats(feats)
    for cell in x.get("approved_cells",[]) or []:
        if _norm_feats(cell.get("feats"))==wanted:
            return cell.get("form")
    return None

def cell_generation_ready(lemma,feats,form=None,path="config/morphology_review.yaml"):
    """Approve only an exact reviewed cell; optionally require its surface form."""
    approved=approved_form(lemma,feats,path)
    if approved is None:
        return False
    return form is None or str(form).casefold()==str(approved).casefold()

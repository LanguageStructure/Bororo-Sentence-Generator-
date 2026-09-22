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

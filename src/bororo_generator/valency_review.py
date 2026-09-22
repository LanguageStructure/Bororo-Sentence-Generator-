"""Human-reviewed lexical coding-frame registry."""
from pathlib import Path
import yaml

DEFAULT=Path("config/valency_review.yaml")

def load_valency_review(path=DEFAULT):
    with open(path,encoding="utf-8") as f:
        return yaml.safe_load(f) or {}

def valency_entry(lemma,path=DEFAULT):
    return load_valency_review(path).get("lexemes",{}).get(lemma)

def reviewed_frame(lemma,path=DEFAULT):
    e=valency_entry(lemma,path)
    if not e or e.get("status")!="reviewed": return None
    return e.get("frame")

def generation_frame_ready(lemma,path=DEFAULT):
    return reviewed_frame(lemma,path) is not None

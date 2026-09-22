"""Structured public result for controlled generation.

Separates a surface candidate from the evidence that licensed it.  This makes
blocked outputs inspectable without inventing a sentence.
"""
from dataclasses import asdict
from .generate import generate_declarative
from .valency_review import valency_entry
from .person_index import reviewed_stem_class

def generate_record(lemma, **kwargs):
    r=generate_declarative(lemma,**kwargs)
    val=valency_entry(lemma) or {}
    evidence={
        "lemma":lemma,
        "reviewed_frame":r.frame,
        "reviewed_stem_class":reviewed_stem_class(lemma),
        "valency_evidence":val.get("evidence"),
        "selected_oblique":val.get("selected_oblique"),
    }
    if r.blocked:
        return {
            "status":"blocked",
            "text":None,
            "evidence":evidence,
            "reasons":r.reasons,
        }
    rec=r.candidate.record()
    return {
        "status":"generated",
        "text":rec["text"],
        "evidence":evidence,
        "provenance":rec["provenance"],
        "validation":rec["validation"],
    }

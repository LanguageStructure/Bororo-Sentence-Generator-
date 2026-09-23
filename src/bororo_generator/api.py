"""Structured public result for controlled generation.

Separates a surface candidate from the evidence that licensed it.  This makes
blocked outputs inspectable without inventing a sentence.
"""
from dataclasses import asdict
from .generate import generate_declarative
from .valency_review import valency_entry
from .person_index import reviewed_stem_class, reviewed_person_cell
from .evidence_layers import evidence_layers

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
        record={
            "status":"blocked",
            "text":None,
            "evidence":evidence,
            "reasons":r.reasons,
        }
        return record
    rec=r.candidate.record()
    record={
        "status":"generated",
        "text":rec["text"],
        "predicate_form":rec.get("predicate_form"),
        "evidence":evidence,
        "provenance":rec["provenance"],
        "validation":rec["validation"],
    }
    # Request information is attached by batch generation; expose the generic
    # layer here without pretending that an exact person cell is known yet.
    record["evidence_layers"]=evidence_layers(record)
    return record

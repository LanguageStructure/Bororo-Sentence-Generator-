"""Scoring utilities for frozen AI experiment v1.

Direct-output scoring is deliberately conservative: automatic checks can flag
observable conflicts with the frozen reviewed inventory, but they do not infer
new Bororo analyses from model output.
"""
from dataclasses import asdict
from .orthography import normalize_bororo
from .person_index import reviewed_person_cell, reviewed_stem_class
from .morphotactics import exclusive_suffix_violations

def score_direct_output(task, surface):
    labels=[]; notes=[]
    surface=(surface or "").strip()
    if not surface:
        labels.append("empty_output")
        return {"task_id":task["task_id"],"condition":"direct","surface":surface,"labels":labels,"notes":notes}
    if surface != normalize_bororo(surface):
        labels.append("orthography_violation")
    # Do not guess segmentation/person from an arbitrary LLM string. Exact
    # grammatical violation labels require reviewed analysis or later audit.
    labels.append("needs_linguistic_audit")
    return {"task_id":task["task_id"],"condition":"direct","surface":surface,"labels":labels,"notes":notes}

def suffix_slot_conflict(reviewed_suffixes):
    """Score only an externally reviewed segmentation; never segment automatically."""
    bad=exclusive_suffix_violations(reviewed_suffixes)
    return {"violation":bool(bad),"conflicting_suffixes":bad}

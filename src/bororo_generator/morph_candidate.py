"""Create explicitly marked generated morphology candidates.

These are morphological forms, not claims that a complete Bororo sentence is grammatical.
Only the reviewed compositional realizer is used.
"""
from .candidate import Candidate
from .provenance import Provenance
from .compositional import realize_ako

def ako_candidate(**features):
    form=realize_ako(**features)
    if form is None:
        return None
    labels=[f"{k}={v}" for k,v in sorted(features.items()) if k!="review_path" and v is not None]
    return Candidate(form,Provenance(
        status="generated",
        pattern="reviewed compositional morphology: ako",
        rules=["human_reviewed_morphology","exact_reviewed_cell"],
        notes=[
            "morphological realization only; not a complete sentence",
            "features: "+", ".join(labels),
        ],
    ))

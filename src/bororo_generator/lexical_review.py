"""Human lexical-review states, separate from corpus evidence.

These labels control review workflow only. They do not infer grammatical facts.
"""
LEXICAL_REVIEW = {
    "aregodu": {
        "status": "frame_pending",
        "reviewed_stem_class": "O",
        "note": "Stem class reviewed independently; coding frame still requires explicit review."
    },
    "tu": {
        "status": "construction_ambiguity",
        "note": "Corpus lemma groups verbal forms with non-verbal annotations; do not treat as one productive paradigm."
    },
    "ro": {
        "status": "construction_ambiguity",
        "note": "Form/function distribution requires construction-level review before generation."
    },
    "rekodu": {
        "status": "construction_ambiguity",
        "note": "Corpus includes verbal and nominally annotated uses; keep unresolved."
    },
    "aidu": {
        "status": "construction_ambiguity",
        "note": "Attested across several constructions/operators; coding frame not yet reviewed."
    },
}

def lexical_review(lemma):
    return LEXICAL_REVIEW.get(lemma)

def review_status(lemma, frame=None, stem_class=None):
    explicit=lexical_review(lemma)
    if explicit:
        return explicit["status"]
    if frame is not None and stem_class is not None:
        return "ready"
    if frame is None and stem_class is not None:
        return "frame_pending"
    if frame is not None and stem_class is None:
        return "stem_class_pending"
    return "analysis_pending"

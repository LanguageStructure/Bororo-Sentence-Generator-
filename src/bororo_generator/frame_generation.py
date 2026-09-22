"""Conservative realization of reviewed declarative predicate frames.

This layer combines only independently reviewed facts:
- lexical coding frame;
- reviewed stem class/person index;
- declarative -re for ordinary monovalent predication.

It does not yet synthesize divalent A expressions or extended-intransitive
obliques; those require additional constructional choices.
"""
from .person_index import indexed_reviewed_stem
from .valency_review import reviewed_frame
from .candidate import Candidate
from .provenance import Provenance

def monovalent_declarative(lemma, person, valency_path="config/valency_review.yaml"):
    if reviewed_frame(lemma,valency_path)!="monovalent":
        return None
    stem=indexed_reviewed_stem(lemma,person)
    if stem is None:
        return None
    return Candidate(stem+"re",Provenance(
        status="generated",
        pattern="reviewed monovalent declarative: S=LEX-re",
        rules=["reviewed_coding_frame","reviewed_stem_class","declarative_re"],
        notes=[f"lemma={lemma}",f"S={person}",
               "Controlled morphological predicate candidate; no overt RP generated."],
    ))

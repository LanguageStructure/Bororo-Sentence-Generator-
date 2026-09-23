"""Conservative realization of reviewed indicative predicate frames.

This layer combines only independently reviewed facts:
- lexical coding frame;
- reviewed stem-class paradigm or exact reviewed person cell;
- indicative -re for ordinary monovalent predication.

It does not yet synthesize divalent A expressions or extended-intransitive
obliques; those require additional constructional choices.
"""
from .person_index import indexed_reviewed_stem
from .valency_review import reviewed_frame
from .candidate import Candidate
from .provenance import Provenance

def monovalent_indicative(lemma, person, valency_path="config/valency_review.yaml"):
    if reviewed_frame(lemma,valency_path)!="monovalent":
        return None
    stem=indexed_reviewed_stem(lemma,person)
    if stem is None:
        return None
    predicate=stem+"re"
    return Candidate(predicate,Provenance(
        status="generated",
        pattern="reviewed monovalent indicative: S=LEX-re",
        rules=["reviewed_coding_frame","reviewed_person_cell_or_class","indicative_re"],
        notes=[f"lemma={lemma}",f"S={person}",
               "Controlled morphological predicate candidate; no overt RP generated."],
    ),predicate_form=predicate)

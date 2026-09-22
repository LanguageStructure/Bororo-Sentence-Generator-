"""Automatic review matrices for lexemes with independently reviewed evidence."""
from .person_index import INDEXES, reviewed_stem_class
from .valency_review import reviewed_frame
from .batch import generate_batch
from .a_host import reviewed_a_persons

PERSONS=("1SG","2SG","3SG","1PL.INCL","1PL.EXCL","2PL","3PL","CORF")

def paradigm_requests(lemma):
    frame=reviewed_frame(lemma)
    cls=reviewed_stem_class(lemma)
    if frame is None or cls is None:
        return []
    persons=[p for p in PERSONS if p in INDEXES[cls]]
    if frame=="monovalent":
        return [{"lemma":lemma,"s_person":p} for p in persons]
    # Extended-intransitive paradigms here cover the core S predicate only.
    # Oblique phrases are generated separately because their lexical content and
    # postposition selection require independent evidence.
    if frame=="extended_intransitive":
        return [{"lemma":lemma,"s_person":p} for p in persons]
    if frame=="divalent":
        # A-host cells are independently reviewed; do not extrapolate them from
        # the lexical predicate stem class.
        return [{"lemma":lemma,"a_person":a,"o_person":o}
                for a in reviewed_a_persons() for o in persons]
    return []

def generate_paradigm(lemma,attestation_index=None):
    return generate_batch(paradigm_requests(lemma),attestation_index)

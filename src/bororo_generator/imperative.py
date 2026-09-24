"""Constructional imperative constraints documented in the grammar draft."""
from .person_index import reviewed_construction_cell
from .valency_review import reviewed_frame
from .candidate import Candidate
from .provenance import Provenance

def positive_imperative(frame):
    # Extended intransitives pattern with monovalents for imperative formation.
    if frame in {"monovalent","extended_intransitive"}:
        return {"addressee_index":"2", "suffix":"-do"}
    if frame=="divalent":
        return {"addressee_index":None, "suffix":None, "note":"predicate retains O-indexing"}
    return None

def negative_imperative(frame):
    if frame in {"monovalent","extended_intransitive"}:
        return {"pattern":"2=LEX-ka-ba"}
    if frame=="divalent":
        return {"pattern":"2A=ka-ba O=LEX"}
    return None


def reviewed_positive_imperative(lemma,person):
    """Generate only an explicitly reviewed imperative surface cell."""
    frame=reviewed_frame(lemma)
    if frame not in {"monovalent","extended_intransitive"}:
        return None
    surface=reviewed_construction_cell(lemma,"imperative",person)
    if surface is None:
        return None
    return Candidate(surface,Provenance(
        status="generated",
        pattern="reviewed positive imperative: 2=LEX-do",
        rules=["reviewed_coding_frame","reviewed_construction_cell","positive_imperative_do"],
        notes=[f"lemma={lemma}",f"addressee={person}",
               "Construction-specific cell; does not license the ordinary declarative paradigm."],
    ),predicate_form=surface)

"""Controlled generation for reviewed divalent declaratives.

Bororo divalent coding is represented constructionally as A=re + O=LEX.
The A index and O index are realized independently; no nominative/accusative
template is assumed.
"""
from .person_index import indexed_reviewed_stem, reviewed_stem_class
from .a_host import reviewed_a_declarative
from .valency_review import reviewed_frame
from .candidate import Candidate
from .provenance import Provenance

def divalent_declarative(
    lemma, a_person, o_person,
    overt_a=None, overt_o=None,
    valency_path="config/valency_review.yaml"
):
    if reviewed_frame(lemma,valency_path)!="divalent":
        return None
    if reviewed_stem_class(lemma) is None:
        return None
    pred=indexed_reviewed_stem(lemma,o_person)
    a_host=reviewed_a_declarative(a_person)
    if pred is None or a_host is None:
        return None
    parts=[]
    if overt_a: parts.append(overt_a.strip())
    parts.append(a_host)
    if overt_o: parts.append(overt_o.strip())
    parts.append(pred)
    return Candidate(" ".join(parts),Provenance(
        status="generated",
        pattern="reviewed divalent declarative: (RP-A) A=re (RP-O) O=LEX",
        rules=["reviewed_divalent_frame","reviewed_stem_class","reviewed_A_declarative_host","O_predicate_index"],
        notes=[f"lemma={lemma}",f"A={a_person}",f"O={o_person}",
               "A and O are kept as distinct coding positions."],
    ))

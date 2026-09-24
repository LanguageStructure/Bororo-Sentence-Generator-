"""Controlled generation for reviewed divalent indicatives.

Bororo divalent coding is represented constructionally as A=re + O=LEX.
The A index and O index are realized independently; no nominative/accusative
template is assumed.
"""
from .person_index import indexed_reviewed_stem
from .a_host import reviewed_a_indicative
from .valency_review import reviewed_frame
from .candidate import Candidate
from .provenance import Provenance

def divalent_indicative(
    lemma, a_person, o_person,
    overt_a=None, overt_o=None,
    valency_path="config/valency_review.yaml"
):
    if reviewed_frame(lemma,valency_path)!="divalent":
        return None
    pred=indexed_reviewed_stem(lemma,o_person)
    a_host=reviewed_a_indicative(a_person)
    if pred is None or a_host is None:
        return None
    parts=[]
    if overt_a: parts.append(overt_a.strip())
    parts.append(a_host)
    if overt_o: parts.append(overt_o.strip())
    parts.append(pred)
    return Candidate(" ".join(parts),Provenance(
        status="generated",
        pattern="reviewed divalent indicative: (RP-A) A=re (RP-O) O=LEX",
        rules=["reviewed_divalent_frame","reviewed_person_cell_or_class","reviewed_A_indicative_host","O_predicate_index"],
        notes=[f"lemma={lemma}",f"A={a_person}",f"O={o_person}",
               "A and O are kept as distinct coding positions."],
    ),predicate_form=pred)

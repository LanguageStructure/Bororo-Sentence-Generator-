"""Controlled generation for reviewed divalent declaratives.

Bororo divalent coding is represented constructionally as A=re + O=LEX.
The A index and O index are realized independently; no nominative/accusative
template is assumed.
"""
from .person_index import indexed_reviewed_stem, INDEXES, reviewed_stem_class
from .valency_review import reviewed_frame
from .candidate import Candidate
from .provenance import Provenance

def _a_declarative(person):
    # A uses the ordinary bound person series as an independent operator host.
    # Surface realization is licensed only where the index value is explicit.
    # For vowel-initial lexical stems, stem-class allomorphy is irrelevant here.
    basic=INDEXES["C"].get(person)
    if basic is None:
        return None
    return basic+"re"

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
    a_host=_a_declarative(a_person)
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
        rules=["reviewed_divalent_frame","reviewed_stem_class","A_declarative_host","O_predicate_index"],
        notes=[f"lemma={lemma}",f"A={a_person}",f"O={o_person}",
               "A and O are kept as distinct coding positions."],
    ))

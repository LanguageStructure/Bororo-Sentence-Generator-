"""Conservative lexical recombination over trusted attested UD structures.

This module does not create new syntactic structures. A substitution is licensed
only when donor and target tokens share UPOS and dependency relation, and the
candidate retains explicit provenance to both source sentences.
"""
from dataclasses import dataclass
from typing import Optional
from .candidate import Candidate
from .provenance import Provenance

@dataclass
class Substitution:
    target_index:int
    old_form:str
    new_form:str
    upos:str
    deprel:str
    donor_sent_id:str
    donor_index:int

def compatible(target, donor):
    return (
        target.get("upos") not in (None,"_")
        and target.get("upos")==donor.get("upos")
        and target.get("deprel")==donor.get("deprel")
        and isinstance(target.get("id"),int)
        and isinstance(donor.get("id"),int)
    )

def recombine(target_sentence, donor_sentence, target_index:int, donor_index:int,
              source_version:Optional[str]=None):
    t=next((x for x in target_sentence.tokens if x.get("id")==target_index),None)
    d=next((x for x in donor_sentence.tokens if x.get("id")==donor_index),None)
    if t is None or d is None:
        raise ValueError("target or donor token not found")
    if not compatible(t,d):
        raise ValueError("substitution rejected: UPOS/deprel mismatch")
    forms=[str(x.get("form","")) for x in target_sentence.tokens if isinstance(x.get("id"),int)]
    integer_tokens=[x for x in target_sentence.tokens if isinstance(x.get("id"),int)]
    pos=integer_tokens.index(t)
    forms[pos]=str(d.get("form",""))
    sub=Substitution(target_index,str(t.get("form","")),str(d.get("form","")),
                     str(t.get("upos","")),str(t.get("deprel","")),
                     donor_sentence.sent_id,donor_index)
    prov=Provenance(status="recombined",source_version=source_version,
        source_sent_ids=[target_sentence.sent_id,donor_sentence.sent_id],
        pattern="attested structure with compatible lexical substitution",
        substitutions=[sub.__dict__],
        rules=["same_upos","same_deprel"],
        notes=["Experimental candidate; morphology/agreement not yet validated."])
    return Candidate(" ".join(forms),prov)

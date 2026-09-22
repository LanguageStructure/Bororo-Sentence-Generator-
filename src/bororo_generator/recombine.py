"""Conservative lexical recombination over trusted attested UD structures.

A substitution is only a candidate. Lemma, surface form and morphology remain
distinct, and no substitution is licensed as grammatical merely by UPOS/DEPREL.
"""
from dataclasses import dataclass
from typing import Optional
from .candidate import Candidate
from .provenance import Provenance

@dataclass
class Substitution:
    target_index:int;old_form:str;new_form:str;old_lemma:str;new_lemma:str
    upos:str;deprel:str;donor_sent_id:str;donor_index:int

def compatible(target,donor):
    return (target.get("upos") not in (None,"_")
        and str(target.get("upos")).strip().upper()==str(donor.get("upos")).strip().upper()
        and target.get("deprel")==donor.get("deprel")
        and target.get("feats")==donor.get("feats")
        and isinstance(target.get("id"),int) and isinstance(donor.get("id"),int))

def recombine(target_sentence,donor_sentence,target_index:int,donor_index:int,
              source_version:Optional[str]=None):
    t=next((x for x in target_sentence.tokens if x.get("id")==target_index),None)
    d=next((x for x in donor_sentence.tokens if x.get("id")==donor_index),None)
    if t is None or d is None:raise ValueError("target or donor token not found")
    if not compatible(t,d):raise ValueError("substitution rejected: UPOS/DEPREL/FEATS mismatch")
    integer_tokens=[x for x in target_sentence.tokens if isinstance(x.get("id"),int)]
    forms=[str(x.get("form","")) for x in integer_tokens];pos=integer_tokens.index(t)
    forms[pos]=str(d.get("form",""))
    sub=Substitution(target_index,str(t.get("form","")),str(d.get("form","")),
        str(t.get("lemma","")),str(d.get("lemma","")),str(t.get("upos","")).strip().upper(),
        str(t.get("deprel","")),donor_sentence.sent_id,donor_index)
    prov=Provenance(status="recombined",source_version=source_version,
        source_sent_ids=[target_sentence.sent_id,donor_sentence.sent_id],
        pattern="attested structure with same UPOS, DEPREL and FEATS",
        substitutions=[sub.__dict__],rules=["same_upos","same_deprel","same_feats"],
        notes=["Experimental candidate; passing annotation constraints is not a grammaticality judgment."])
    return Candidate(" ".join(forms),prov)

"""Attested morphosyntactic slots.

A slot keeps lemma, surface form and syntactic environment separate. This is
descriptive evidence; it does not by itself license generation.
"""
from dataclasses import dataclass,asdict
from collections import defaultdict

@dataclass(frozen=True)
class Slot:
    lemma:str
    form:str
    upos:str
    deprel:str
    head_lemma:str
    head_upos:str
    sent_id:str
    token_id:int

    def to_dict(self): return asdict(self)

def sentence_slots(sentence):
    ints={t["id"]:t for t in sentence.tokens if isinstance(t.get("id"),int)}
    out=[]
    for t in ints.values():
        head=ints.get(t.get("head"))
        out.append(Slot(
            lemma=str(t.get("lemma") or "_"),
            form=str(t.get("form") or "_"),
            upos=str(t.get("upos") or "_").strip().upper(),
            deprel=str(t.get("deprel") or "_"),
            head_lemma=str(head.get("lemma") or "_") if head else "ROOT",
            head_upos=str(head.get("upos") or "_").strip().upper() if head else "ROOT",
            sent_id=sentence.sent_id,token_id=t["id"]))
    return out

def lemma_realizations(sentences):
    data=defaultdict(lambda:defaultdict(list))
    for s in sentences:
        for slot in sentence_slots(s):
            data[slot.lemma][slot.form].append(slot)
    return data

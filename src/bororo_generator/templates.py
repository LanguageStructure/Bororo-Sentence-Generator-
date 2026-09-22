"""Descriptive templates extracted from attested trusted sentences.

Templates preserve token-level morphology and syntax. They are evidence objects,
not generation rules.
"""
from dataclasses import dataclass,asdict

@dataclass
class TemplateToken:
    id:int;form:str;lemma:str;upos:str;feats:object;head:int;deprel:str

@dataclass
class AttestedTemplate:
    sent_id:str;text:str;tokens:list
    def to_dict(self):
        return {"sent_id":self.sent_id,"text":self.text,
                "tokens":[asdict(t) for t in self.tokens]}

def from_sentence(s):
    toks=[]
    for t in s.tokens:
        if not isinstance(t.get("id"),int):continue
        toks.append(TemplateToken(t["id"],str(t.get("form") or "_"),
            str(t.get("lemma") or "_"),str(t.get("upos") or "_").strip().upper(),
            t.get("feats"),int(t.get("head") or 0),str(t.get("deprel") or "_")))
    return AttestedTemplate(s.sent_id,s.text,toks)

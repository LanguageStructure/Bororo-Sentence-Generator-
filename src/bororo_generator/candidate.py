"""Serializable candidate sentence object."""
from dataclasses import dataclass,asdict
from typing import Optional
from .provenance import Provenance
from .validator import validate_candidate
from .orthography import normalize_bororo

@dataclass
class Candidate:
    text:str
    provenance:Provenance
    predicate_form:Optional[str]=None

    def __post_init__(self):
        # Generated/recombined Bororo output is always in project orthography.
        self.text=normalize_bororo(self.text)
        if self.predicate_form is not None:
            self.predicate_form=normalize_bororo(self.predicate_form)

    def record(self):
        result=validate_candidate(self.text,self.provenance)
        return {"text":self.text,"predicate_form":self.predicate_form,"provenance":self.provenance.to_dict(),
                "validation":asdict(result)}

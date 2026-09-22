"""Serializable candidate sentence object."""
from dataclasses import dataclass,asdict
from .provenance import Provenance
from .validator import validate_candidate
from .orthography import normalize_bororo

@dataclass
class Candidate:
    text:str
    provenance:Provenance

    def __post_init__(self):
        # Generated/recombined Bororo output is always in project orthography.
        self.text=normalize_bororo(self.text)

    def record(self):
        result=validate_candidate(self.text,self.provenance)
        return {"text":self.text,"provenance":self.provenance.to_dict(),
                "validation":asdict(result)}

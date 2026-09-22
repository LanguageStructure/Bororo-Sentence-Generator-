"""Serializable candidate sentence object."""
from dataclasses import dataclass,asdict
from .provenance import Provenance
from .validator import validate_candidate

@dataclass
class Candidate:
    text:str
    provenance:Provenance

    def record(self):
        result=validate_candidate(self.text,self.provenance)
        return {"text":self.text,"provenance":self.provenance.to_dict(),
                "validation":asdict(result)}

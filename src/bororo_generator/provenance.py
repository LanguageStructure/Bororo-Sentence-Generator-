"""Provenance records for experimental Bororo outputs."""
from dataclasses import dataclass,field,asdict
from typing import List,Optional

VALID_STATUSES={"attested","recombined","generated"}

@dataclass
class Provenance:
    status:str
    source_version:Optional[str]=None
    source_sent_ids:List[str]=field(default_factory=list)
    pattern:Optional[str]=None
    substitutions:List[dict]=field(default_factory=list)
    rules:List[str]=field(default_factory=list)
    notes:List[str]=field(default_factory=list)

    def validate(self):
        if self.status not in VALID_STATUSES:
            raise ValueError(f"invalid provenance status: {self.status}")
        if self.status=="attested" and not self.source_sent_ids:
            raise ValueError("attested output requires source_sent_ids")
        if self.status=="recombined" and (not self.source_sent_ids or not self.substitutions):
            raise ValueError("recombined output requires source_sent_ids and substitutions")
        if self.status=="generated" and not (self.pattern or self.rules):
            raise ValueError("generated output requires a pattern or explicit rules")
        return True

    def to_dict(self):
        self.validate()
        return asdict(self)

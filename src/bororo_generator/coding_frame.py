"""Bororo participant-coding frames reviewed from the grammar draft.

Frames are morphosyntactic, not inferred from English/Portuguese translation
or from semantic participant count.
"""
from dataclasses import dataclass
from typing import Optional

@dataclass(frozen=True)
class CodingFrame:
    name: str
    core_roles: tuple
    predicate_index_role: str
    operator_host_role: str
    oblique_role: Optional[str]=None
    oblique_marker: Optional[str]=None

MONOVALENT=CodingFrame("monovalent",("S",),"S","S")
DIVALENT=CodingFrame("divalent",("A","O"),"O","A")
EXTENDED_INTRANSITIVE=CodingFrame(
    "extended_intransitive",("S",),"S","S",
    oblique_role="additional_participant",oblique_marker=None
)

FRAMES={x.name:x for x in (MONOVALENT,DIVALENT,EXTENDED_INTRANSITIVE)}

def coding_frame(name):
    return FRAMES.get(name)

def declarative_schema(name):
    f=coding_frame(name)
    if f is None: return None
    if name=="monovalent": return "(RP) S=LEX-re"
    if name=="divalent": return "(RP-A) A=re (RP-O) O=LEX"
    if name=="extended_intransitive": return "(RP) S=LEX-re ... RP POSTP"

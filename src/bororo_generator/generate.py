"""Single evidence-bound dispatcher for reviewed Bororo predicate generation.

Selection is lexical: the reviewed coding frame chooses the structural generator.
Unknown or incompletely reviewed combinations return a blocked result rather
than falling back to another frame.
"""
from dataclasses import dataclass, field
from typing import Optional
from .valency_review import reviewed_frame
from .frame_generation import monovalent_declarative
from .extended_generation import extended_intransitive_declarative
from .divalent_generation import divalent_declarative

@dataclass
class DispatchResult:
    candidate: Optional[object]
    frame: Optional[str]
    blocked: bool
    reasons: list[str]=field(default_factory=list)

def generate_declarative(
    lemma, *, s_person=None, a_person=None, o_person=None,
    oblique_phrase=None, overt_a=None, overt_o=None,
    valency_path="config/valency_review.yaml"
):
    frame=reviewed_frame(lemma,valency_path)
    if frame is None:
        return DispatchResult(None,None,True,["no reviewed coding frame"])

    if frame=="monovalent":
        if s_person is None:
            return DispatchResult(None,frame,True,["S person required"])
        c=monovalent_declarative(lemma,s_person,valency_path)
    elif frame=="extended_intransitive":
        if s_person is None:
            return DispatchResult(None,frame,True,["S person required"])
        c=extended_intransitive_declarative(
            lemma,s_person,oblique_phrase,valency_path
        )
    elif frame=="divalent":
        if a_person is None or o_person is None:
            return DispatchResult(None,frame,True,["A and O persons required"])
        c=divalent_declarative(
            lemma,a_person,o_person,overt_a,overt_o,valency_path
        )
    else:
        return DispatchResult(None,frame,True,[f"unsupported reviewed frame: {frame}"])

    if c is None:
        return DispatchResult(
            None,frame,True,
            ["frame reviewed, but required morphology/constructional evidence is incomplete"]
        )
    return DispatchResult(c,frame,False,[])

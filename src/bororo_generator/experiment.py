"""Frozen schemas and scoring primitives for the AI proposal experiment.

This module does not call an LLM. It defines the task/proposal boundary before
experimental outputs are collected.
"""
from dataclasses import dataclass, asdict, field
from typing import Optional
from .valency_review import reviewed_frame
from .generate import generate_indicative

@dataclass(frozen=True)
class ExperimentTask:
    task_id: str
    lemma: str
    construction: str = "indicative"
    s_person: Optional[str] = None
    a_person: Optional[str] = None
    o_person: Optional[str] = None
    oblique_phrase: Optional[str] = None

@dataclass(frozen=True)
class StructuralProposal:
    lemma: str
    construction: str
    s_person: Optional[str] = None
    a_person: Optional[str] = None
    o_person: Optional[str] = None
    oblique_phrase: Optional[str] = None

@dataclass
class ProposalScore:
    task_id: str
    condition: str
    blocked: bool
    generated_text: Optional[str]
    labels: list[str] = field(default_factory=list)
    reasons: list[str] = field(default_factory=list)

def proposal_from_task(task):
    return StructuralProposal(task.lemma,task.construction,task.s_person,task.a_person,task.o_person,task.oblique_phrase)

def score_bounded_proposal(task, proposal, valency_path="config/valency_review.yaml"):
    labels=[]
    reasons=[]
    if proposal.lemma != task.lemma:
        labels.append("task_mismatch")
    expected_frame=reviewed_frame(proposal.lemma,valency_path)
    if expected_frame is None:
        labels.append("unsupported_but_plausible")
    if proposal.construction != "indicative":
        # v1 dispatcher intentionally realizes only ordinary indicative requests.
        labels.append("unsupported_but_plausible")
        return ProposalScore(task.task_id,"evidence_bounded",True,None,sorted(set(labels)),["construction not realized by frozen v1 dispatcher"])
    r=generate_indicative(
        proposal.lemma,s_person=proposal.s_person,a_person=proposal.a_person,
        o_person=proposal.o_person,oblique_phrase=proposal.oblique_phrase,
        valency_path=valency_path)
    if r.blocked:
        labels.append("blocked")
        if expected_frame is not None:
            labels.append("unsupported_but_plausible")
        reasons.extend(r.reasons)
        return ProposalScore(task.task_id,"evidence_bounded",True,None,sorted(set(labels)),reasons)
    return ProposalScore(task.task_id,"evidence_bounded",False,r.candidate.text,sorted(set(labels)),reasons)

def record(task, proposal, score):
    return {"task":asdict(task),"proposal":asdict(proposal),"score":asdict(score)}

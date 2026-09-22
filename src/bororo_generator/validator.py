"""Validation gate for candidate sentences.

This module validates documentary/procedural evidence. It does not claim native-speaker
grammaticality. Community/specialist review remains a separate layer.
"""
from dataclasses import dataclass,field
from typing import List
from .provenance import Provenance

@dataclass
class ValidationResult:
    accepted:bool
    checks:dict
    warnings:List[str]=field(default_factory=list)

def validate_candidate(text:str,provenance:Provenance)->ValidationResult:
    checks={}
    warnings=[]
    checks["nonempty_text"]=bool(text and text.strip())
    try:
        provenance.validate();checks["valid_provenance"]=True
    except ValueError as e:
        checks["valid_provenance"]=False;warnings.append(str(e))
    # Generation is deliberately blocked unless evidence is explicit.
    checks["evidence_present"]=bool(provenance.source_sent_ids or provenance.pattern or provenance.rules)
    if provenance.status!="attested":
        warnings.append("experimental output: not an attested CorBo sentence")
    return ValidationResult(all(checks.values()),checks,warnings)

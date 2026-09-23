"""Corpus evidence layer for generated predicate forms.

Corpus occurrence is observational evidence only. It never promotes a cell to
human-reviewed grammar and never licenses generation by itself.
"""
from .orthography import form_key
from .person_index import reviewed_stem_class, reviewed_person_cell

def corpus_form_evidence(record):
    att=record.get("attestation",{}) or {}
    if record.get("status")!="generated":
        return {"level":"none","attested":False,"form":None,"sent_ids":[]}
    form=att.get("predicate_form") or record.get("predicate_form")
    ids=list(dict.fromkeys(att.get("predicate_source_sent_ids",[]) or []))
    return {
        "level":"predicate_form",
        "attested":bool(att.get("predicate_form_attested")),
        "form":form,
        "sent_ids":ids,
        "interpretation":"corpus occurrence; not human grammatical review",
    }

def evidence_layers(record):
    ev=record.get("evidence",{}) or {}
    req=record.get("request",{}) or {}
    lemma=req.get("lemma") or ev.get("lemma")
    person=req.get("s_person") or req.get("o_person")
    cls=reviewed_stem_class(lemma) if lemma else None
    exact=reviewed_person_cell(lemma,person) if lemma and person else None
    grammar={
        "reviewed_frame":ev.get("reviewed_frame"),
        "morphology_license":(
            {"type":"exact_person_cell","person":person,"form":exact}
            if exact is not None else
            {"type":"full_stem_class","stem_class":cls}
            if cls is not None else None
        ),
        "valency_evidence":ev.get("valency_evidence"),
    }
    return {
        "reviewed_grammar":grammar,
        "generated_candidate":{
            "status":record.get("status"),
            "text":record.get("text"),
            "predicate_form":record.get("predicate_form"),
        },
        "corpus_evidence":corpus_form_evidence(record),
    }

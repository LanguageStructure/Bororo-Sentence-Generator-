"""Corpus attestation index for generated Bororo surfaces.

Attestation is an evidence label, not a grammaticality judgment. Matching uses
the project's Bororo comparison key and preserves the source sentence ids.
"""
from collections import defaultdict
from .orthography import form_key

def surface_attestation(sentences):
    idx=defaultdict(list)
    for s in sentences:
        text=getattr(s,"text",None)
        sid=getattr(s,"sent_id",None)
        if text and sid:
            idx[form_key(text)].append(sid)
    return dict(idx)

def annotate_attestation(record,index):
    if record.get("status")!="generated" or not record.get("text"):
        return record
    ids=index.get(form_key(record["text"]),[])
    record=dict(record)
    record["attestation"]={
        "attested":bool(ids),
        "source_sent_ids":ids,
        "match":"exact_surface" if ids else None,
    }
    return record

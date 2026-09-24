"""Corpus attestation indexes for generated Bororo outputs.

Sentence-surface and token-form attestation are independent evidence levels.
Neither is a grammaticality judgment.
"""
from collections import defaultdict
from .orthography import form_key

def surface_attestation(sentences):
    idx=defaultdict(list)
    for s in sentences:
        text=getattr(s,"text",None); sid=getattr(s,"sent_id",None)
        if text and sid: idx[form_key(text)].append(sid)
    return {k:list(dict.fromkeys(v)) for k,v in idx.items()}

def token_attestation(sentences):
    idx=defaultdict(list)
    for s in sentences:
        sid=getattr(s,"sent_id",None)
        for t in getattr(s,"tokens",()) or ():
            form=t.get("form")
            if form and sid: idx[form_key(str(form))].append(sid)
    return {k:list(dict.fromkeys(v)) for k,v in idx.items()}

def annotate_attestation(record,surface_index=None,token_index=None):
    if record.get("status")!="generated" or not record.get("text"):
        return record
    record=dict(record)
    text=record["text"]
    sids=(surface_index or {}).get(form_key(text),[])
    # Prefer the predicate constituent supplied by generation. The final-token
    # fallback is retained only for legacy records.
    predicate=record.get("predicate_form") or (text.split()[-1] if text.split() else text)
    tids=(token_index or {}).get(form_key(predicate),[])
    record["attestation"]={
        "sentence_attested":bool(sids),
        "sentence_source_sent_ids":sids,
        "predicate_form":predicate,
        "predicate_form_attested":bool(tids),
        "predicate_source_sent_ids":tids,
    }
    return record

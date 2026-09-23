"""Generate review batches and optionally compare them with CorBo."""
from .api import generate_record
from .attestation import surface_attestation,token_attestation,annotate_attestation
from .corpus import read_conllu
from .evidence_layers import evidence_layers

def generate_batch(requests, attestation_index=None, token_index=None):
    """Generate requested cells; optionally annotate exact CorBo surface matches."""
    out=[]
    for i,req in enumerate(requests,1):
        req=dict(req)
        lemma=req.pop("lemma")
        rec=generate_record(lemma,**req)
        if attestation_index is not None:
            rec=annotate_attestation(rec,attestation_index,token_index)
        rec["request_id"]=i
        rec["request"]={"lemma":lemma,**req}
        # Recompute after the request is attached so morphology provenance can
        # distinguish an exact reviewed cell from a full stem-class license.
        rec["evidence_layers"]=evidence_layers(rec)
        out.append(rec)
    return out

def generate_batch_against_corpus(requests, corpus_path):
    sentences=list(read_conllu(corpus_path))
    sidx=surface_attestation(sentences)
    tidx=token_attestation(sentences)
    return generate_batch(requests,sidx,tidx)

def batch_summary(records):
    counts={"generated":0,"blocked":0,"accepted":0,
            "sentence_attested":0,"predicate_form_attested":0,"generated_unattested":0}
    for r in records:
        counts[r["status"]]=counts.get(r["status"],0)+1
        if r.get("validation",{}).get("accepted"): counts["accepted"]+=1
        if r.get("status")=="generated":
            att=r.get("attestation",{})
            if att.get("sentence_attested"): counts["sentence_attested"]+=1
            if att.get("predicate_form_attested"): counts["predicate_form_attested"]+=1
            if "attestation" in r and not att.get("sentence_attested") and not att.get("predicate_form_attested"):
                counts["generated_unattested"]+=1
    counts["total"]=len(records)
    return counts

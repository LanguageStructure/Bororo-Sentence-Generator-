"""Generate review batches and optionally compare them with CorBo."""
from .api import generate_record
from .attestation import surface_attestation,annotate_attestation
from .corpus import read_conllu

def generate_batch(requests, attestation_index=None):
    """Generate requested cells; optionally annotate exact CorBo surface matches."""
    out=[]
    for i,req in enumerate(requests,1):
        req=dict(req)
        lemma=req.pop("lemma")
        rec=generate_record(lemma,**req)
        if attestation_index is not None:
            rec=annotate_attestation(rec,attestation_index)
        rec["request_id"]=i
        rec["request"]={"lemma":lemma,**req}
        out.append(rec)
    return out

def generate_batch_against_corpus(requests, corpus_path):
    idx=surface_attestation(read_conllu(corpus_path))
    return generate_batch(requests,idx)

def batch_summary(records):
    counts={"generated":0,"blocked":0,"accepted":0,
            "corpus_attested":0,"generated_unattested":0}
    for r in records:
        counts[r["status"]]=counts.get(r["status"],0)+1
        if r.get("validation",{}).get("accepted"): counts["accepted"]+=1
        if r.get("status")=="generated":
            if r.get("attestation",{}).get("attested"):
                counts["corpus_attested"]+=1
            elif "attestation" in r:
                counts["generated_unattested"]+=1
    counts["total"]=len(records)
    return counts

"""Generate a review batch from explicitly requested controlled cells."""
from .api import generate_record

def generate_batch(requests):
    """Requests are dicts accepted by generate_record, each requiring lemma."""
    out=[]
    for i,req in enumerate(requests,1):
        req=dict(req)
        lemma=req.pop("lemma")
        rec=generate_record(lemma,**req)
        rec["request_id"]=i
        rec["request"]={"lemma":lemma,**req}
        out.append(rec)
    return out

def batch_summary(records):
    counts={"generated":0,"blocked":0,"accepted":0}
    for r in records:
        counts[r["status"]]=counts.get(r["status"],0)+1
        if r.get("validation",{}).get("accepted"): counts["accepted"]+=1
    counts["total"]=len(records)
    return counts

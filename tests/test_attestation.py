from dataclasses import dataclass
from bororo_generator.attestation import surface_attestation,annotate_attestation

@dataclass
class S:
    sent_id:str
    text:str

def test_exact_surface_attestation():
    idx=surface_attestation([S("x1","Unudure"),S("x2","amerure")])
    r=annotate_attestation({"status":"generated","text":"unudure"},idx)
    assert r["attestation"]["attested"]
    assert r["attestation"]["source_sent_ids"]==["x1"]

def test_unattested_remains_generated():
    idx=surface_attestation([S("x1","unudure")])
    r=annotate_attestation({"status":"generated","text":"ikodure"},idx)
    assert not r["attestation"]["attested"]
    assert r["status"]=="generated"

def test_blocked_is_not_relabelled():
    r={"status":"blocked","text":None}
    assert annotate_attestation(r,{})==r


def test_token_attestation_deduplicates_sent_ids():
    from bororo_generator.attestation import token_attestation
    @dataclass
    class T:
        sent_id:str
        text:str
        tokens:tuple
    s=T("x1","maku maku",({"form":"maku"},{"form":"maku"}))
    assert token_attestation([s])["maku"]==["x1"]

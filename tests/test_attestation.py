from dataclasses import dataclass
from bororo_generator.attestation import surface_attestation,token_attestation,annotate_attestation

@dataclass
class S:
    sent_id:str
    text:str
    tokens:tuple=()

def test_exact_surface_attestation():
    idx=surface_attestation([S("x1","Unudure"),S("x2","amerure")])
    r=annotate_attestation({"status":"generated","text":"unudure"},idx)
    assert r["attestation"]["sentence_attested"]
    assert r["attestation"]["sentence_source_sent_ids"]==["x1"]

def test_unattested_remains_generated():
    idx=surface_attestation([S("x1","unudure")])
    r=annotate_attestation({"status":"generated","text":"ikodure"},idx)
    assert not r["attestation"]["sentence_attested"]
    assert r["status"]=="generated"

def test_blocked_is_not_relabelled():
    r={"status":"blocked","text":None}
    assert annotate_attestation(r,{})==r

def test_token_attestation_deduplicates_sent_ids():
    s=S("x1","maku maku",({"form":"maku"},{"form":"maku"}))
    assert token_attestation([s])["maku"]==["x1"]

def test_structured_predicate_survives_trailing_oblique():
    token_idx={"imakore":["x7"],"ji":["x8"]}
    r=annotate_attestation(
        {"status":"generated","text":"imakore Boe ji","predicate_form":"imakore"},
        token_index=token_idx,
    )
    assert r["attestation"]["predicate_form"]=="imakore"
    assert r["attestation"]["predicate_form_attested"]
    assert r["attestation"]["predicate_source_sent_ids"]==["x7"]

def test_legacy_record_uses_final_token_fallback():
    r=annotate_attestation(
        {"status":"generated","text":"legacy predicate"},
        token_index={"predicate":["x9"]},
    )
    assert r["attestation"]["predicate_form"]=="predicate"
    assert r["attestation"]["predicate_source_sent_ids"]==["x9"]

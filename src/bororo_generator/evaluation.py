"""Paradigm-level empirical evaluation against a supplied CorBo corpus.

Token-form evidence is kept distinct from full structural-cell evidence.
For divalents, O=LEX attestation licenses an O-form only; it does not identify A.
"""
from .attestation import surface_attestation,token_attestation
from .corpus import read_conllu
from .batch import generate_batch
from .paradigm_generation import paradigm_requests
from .evidence_layers import evidence_layers

def evaluate_paradigm(lemma, corpus_path):
    sentences=list(read_conllu(corpus_path))
    sidx=surface_attestation(sentences); tidx=token_attestation(sentences)
    records=generate_batch(paradigm_requests(lemma),sidx,tidx)
    generated=[r for r in records if r.get("status")=="generated"]
    sentence_cells=[r for r in generated if r.get("attestation",{}).get("sentence_attested")]
    form_records=[r for r in generated if r.get("attestation",{}).get("predicate_form_attested")]
    unique_forms={}
    for r in form_records:
        a=r["attestation"]; key=a["predicate_form"]
        unique_forms.setdefault(key,{"form":key,"sent_ids":set(),"requests":[]})
        unique_forms[key]["sent_ids"].update(a.get("predicate_source_sent_ids",[]))
        unique_forms[key]["requests"].append(r.get("request",{}))
    forms=[{"form":v["form"],"sent_ids":sorted(v["sent_ids"]),"requests":v["requests"]}
           for v in unique_forms.values()]
    frame=(records[0].get("evidence",{}).get("reviewed_frame") if records else None)
    full=sum(1 for r in generated if r.get("evidence_layers",{}).get("reviewed_grammar",{}).get("morphology_license",{}).get("type")=="full_stem_class")
    exact=sum(1 for r in generated if r.get("evidence_layers",{}).get("reviewed_grammar",{}).get("morphology_license",{}).get("type")=="exact_person_cell")
    return {
        "lemma":lemma,"frame":frame,
        "structural_cells_requested":len(records),
        "structural_cells_sentence_attested":len(sentence_cells),
        "generated_records":len(generated),
        "predicate_form_records_attested":len(form_records),
        "unique_predicate_forms_attested":len(forms),
        "attested_predicate_forms":forms,
        "blocked":len([r for r in records if r.get("status")=="blocked"]),
        "licensed_by_full_class":full,
        "licensed_by_exact_cell":exact,
        "records":records,
        "evidence_layers":[evidence_layers(r) for r in records],
        "interpretation":(
            "Predicate FORM attestation is morphological evidence only. "
            "For divalents it does not establish the A×O structural cell."
        ),
    }

def evaluate_lexemes(lemmas, corpus_path):
    rows=[evaluate_paradigm(l,corpus_path) for l in lemmas]
    return {
        "lexemes":len(rows),
        "structural_cells_requested":sum(r["structural_cells_requested"] for r in rows),
        "structural_cells_sentence_attested":sum(r["structural_cells_sentence_attested"] for r in rows),
        "generated_records":sum(r["generated_records"] for r in rows),
        "unique_predicate_forms_attested":sum(r["unique_predicate_forms_attested"] for r in rows),
        "blocked":sum(r["blocked"] for r in rows),
        "licensed_by_full_class":sum(r["licensed_by_full_class"] for r in rows),
        "licensed_by_exact_cell":sum(r["licensed_by_exact_cell"] for r in rows),
        "results":rows,
    }

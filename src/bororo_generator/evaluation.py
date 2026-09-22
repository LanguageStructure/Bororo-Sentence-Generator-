"""Paradigm-level empirical evaluation against a supplied CorBo corpus.

Counts describe coverage of generated cells in that corpus. They are not
grammaticality scores and do not treat unattested cells as ill-formed.
"""
from .attestation import surface_attestation,token_attestation
from .corpus import read_conllu
from .paradigm_generation import generate_paradigm

def evaluate_paradigm(lemma, corpus_path):
    sentences=list(read_conllu(corpus_path))
    sidx=surface_attestation(sentences)
    tidx=token_attestation(sentences)
    from .batch import generate_batch
    from .paradigm_generation import paradigm_requests
    records=generate_batch(paradigm_requests(lemma),sidx,tidx)
    generated=[r for r in records if r.get("status")=="generated"]
    sentence_attested=[r for r in generated if r.get("attestation",{}).get("sentence_attested")]
    form_attested=[r for r in generated if r.get("attestation",{}).get("predicate_form_attested")]
    blocked=[r for r in records if r.get("status")=="blocked"]
    return {
        "lemma":lemma,
        "cells_requested":len(records),
        "generated":len(generated),
        "sentence_attested":len(sentence_attested),
        "predicate_form_attested":len(form_attested),
        "generated_unattested":len([r for r in generated if not r.get("attestation",{}).get("sentence_attested") and not r.get("attestation",{}).get("predicate_form_attested")]),
        "blocked":len(blocked),
        "sentence_attestation_rate":(len(sentence_attested)/len(generated) if generated else None),
        "predicate_form_attestation_rate":(len(form_attested)/len(generated) if generated else None),
        "records":records,
        "interpretation":"Corpus coverage only; absence is not evidence of ungrammaticality.",
    }

def evaluate_lexemes(lemmas, corpus_path):
    rows=[evaluate_paradigm(l,corpus_path) for l in lemmas]
    return {
        "lexemes":len(rows),
        "cells_requested":sum(r["cells_requested"] for r in rows),
        "generated":sum(r["generated"] for r in rows),
        "sentence_attested":sum(r["sentence_attested"] for r in rows),
        "predicate_form_attested":sum(r["predicate_form_attested"] for r in rows),
        "generated_unattested":sum(r["generated_unattested"] for r in rows),
        "blocked":sum(r["blocked"] for r in rows),
        "results":rows,
    }

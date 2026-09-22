"""Paradigm-level empirical evaluation against a supplied CorBo corpus.

Counts describe coverage of generated cells in that corpus. They are not
grammaticality scores and do not treat unattested cells as ill-formed.
"""
from .attestation import surface_attestation
from .corpus import read_conllu
from .paradigm_generation import generate_paradigm

def evaluate_paradigm(lemma, corpus_path):
    idx=surface_attestation(read_conllu(corpus_path))
    records=generate_paradigm(lemma,idx)
    generated=[r for r in records if r.get("status")=="generated"]
    attested=[r for r in generated if r.get("attestation",{}).get("attested")]
    blocked=[r for r in records if r.get("status")=="blocked"]
    return {
        "lemma":lemma,
        "cells_requested":len(records),
        "generated":len(generated),
        "corpus_attested":len(attested),
        "generated_unattested":len(generated)-len(attested),
        "blocked":len(blocked),
        "attestation_rate":(len(attested)/len(generated) if generated else None),
        "records":records,
        "interpretation":"Corpus coverage only; absence is not evidence of ungrammaticality.",
    }

def evaluate_lexemes(lemmas, corpus_path):
    rows=[evaluate_paradigm(l,corpus_path) for l in lemmas]
    return {
        "lexemes":len(rows),
        "cells_requested":sum(r["cells_requested"] for r in rows),
        "generated":sum(r["generated"] for r in rows),
        "corpus_attested":sum(r["corpus_attested"] for r in rows),
        "generated_unattested":sum(r["generated_unattested"] for r in rows),
        "blocked":sum(r["blocked"] for r in rows),
        "results":rows,
    }

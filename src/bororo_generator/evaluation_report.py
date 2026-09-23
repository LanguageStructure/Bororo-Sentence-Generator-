"""Compact, reproducible evaluation reports.

Reports summarize existing evaluation evidence; they do not add grammatical
judgments or promote corpus observations to reviewed status.
"""
from datetime import datetime,timezone
from .evaluation import evaluate_lexemes

SCHEMA_VERSION="1.0"

def evaluation_report(lemmas,corpus_path):
    ev=evaluate_lexemes(lemmas,corpus_path)
    return {
        "schema_version":SCHEMA_VERSION,
        "report_type":"controlled_generation_evaluation",
        "corpus_path":str(corpus_path),
        "lemmas":list(lemmas),
        "summary":{
            "lexemes":ev["lexemes"],
            "structural_cells_requested":ev["structural_cells_requested"],
            "structural_cells_sentence_attested":ev["structural_cells_sentence_attested"],
            "generated_records":ev["generated_records"],
            "unique_predicate_forms_attested":ev["unique_predicate_forms_attested"],
            "blocked":ev["blocked"],
        },
        "method":{
            "sentence_attestation":"exact normalized generated surface",
            "predicate_form_attestation":"generated predicate FORM occurs as a corpus token",
            "limits":[
                "predicate-form occurrence is morphological evidence, not grammatical review",
                "for divalents, predicate-token evidence does not resolve A",
                "absence from the supplied corpus is not evidence of ungrammaticality",
            ],
        },
        "results":ev["results"],
    }

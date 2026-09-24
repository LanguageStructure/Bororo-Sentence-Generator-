from bororo_generator.evidence_layers import corpus_form_evidence,evidence_layers

def test_attestation_does_not_become_review():
    r={
        "status":"generated","text":"ikodure","predicate_form":"ikodure",
        "evidence":{"reviewed_frame":"monovalent"},
        "request":{"lemma":"kodu","s_person":"1SG"},
        "attestation":{"predicate_form":"ikodure","predicate_form_attested":True,
                       "predicate_source_sent_ids":["31-3","31-3","73-1"]},
    }
    layers=evidence_layers(r)
    assert layers["corpus_evidence"]["attested"]
    assert layers["corpus_evidence"]["sent_ids"]==["31-3","73-1"]
    assert "reviewed_frame" not in layers["corpus_evidence"]
    assert layers["reviewed_grammar"]["reviewed_frame"]=="monovalent"
    assert layers["reviewed_grammar"]["morphology_license"]=={
        "type":"exact_person_cell","person":"1SG","form":"ikodu"
    }

def test_unattested_form_remains_generated():
    r={"status":"generated","text":"x","predicate_form":"x",
       "evidence":{},"attestation":{"predicate_form_attested":False}}
    layers=evidence_layers(r)
    assert layers["generated_candidate"]["status"]=="generated"
    assert not layers["corpus_evidence"]["attested"]


def test_full_paradigm_license_is_distinct_from_exact_cell():
    r={"status":"generated","text":"unudure","predicate_form":"unudure",
       "request":{"lemma":"nudu","s_person":"3SG"},
       "evidence":{"reviewed_frame":"monovalent"},"attestation":{}}
    lic=evidence_layers(r)["reviewed_grammar"]["morphology_license"]
    assert lic=={"type":"full_stem_class","stem_class":"U"}

from bororo_generator.batch import generate_batch,batch_summary

def test_batch_keeps_generated_and_blocked():
    rs=generate_batch([
        {"lemma":"nudu","s_person":"3SG"},
        {"lemma":"tawuje","a_person":"2SG","o_person":"3PL"},
    ])
    s=batch_summary(rs)
    assert s=={"generated":1,"blocked":1,"accepted":1,
              "sentence_attested":0,"predicate_form_attested":0,
              "generated_unattested":0,"total":2}
    assert rs[0]["request_id"]==1 and rs[1]["request_id"]==2

def test_batch_attestation_summary():
    rs=generate_batch([{"lemma":"nudu","s_person":"3SG"}],{"unudure":["g1"]})
    s=batch_summary(rs)
    assert s["sentence_attested"]==1
    assert s["predicate_form_attested"]==0
    assert s["generated_unattested"]==0
    assert rs[0]["attestation"]["sentence_source_sent_ids"]==["g1"]

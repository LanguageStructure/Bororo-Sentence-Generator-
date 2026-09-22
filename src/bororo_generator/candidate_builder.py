"""Build candidates only from trusted attested templates plus approved morphology."""
from .candidate import Candidate
from .provenance import Provenance
from .generation_gate import check_lemmas

def attested_candidate(sentence,source_version=None):
    """An attested sentence is always displayable with explicit provenance."""
    return Candidate(sentence.text,Provenance(
        status="attested",source_version=source_version,
        source_sent_ids=[sentence.sent_id],
        pattern="attested corpus sentence",substitutions=[],rules=[]))

def generation_gate_for_sentence(sentence,review_path="config/morphology_review.yaml"):
    """Check whether every lexical lemma in a sentence has human approval."""
    lemmas=[]
    for t in sentence.tokens:
        if not isinstance(t.get("id"),int):continue
        upos=str(t.get("upos") or "_").strip().upper()
        lemma=str(t.get("lemma") or "_")
        if upos=="PUNCT" or lemma=="_":continue
        lemmas.append(lemma)
    return check_lemmas(lemmas,review_path)

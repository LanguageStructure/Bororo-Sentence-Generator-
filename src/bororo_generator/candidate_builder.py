"""Build candidates only from trusted attested templates plus approved morphology."""
from .candidate import Candidate
from .provenance import Provenance
from .generation_gate import check_tokens

def attested_candidate(sentence,source_version=None):
    """An attested sentence is always displayable with explicit provenance."""
    return Candidate(sentence.text,Provenance(
        status="attested",source_version=source_version,
        source_sent_ids=[sentence.sent_id],
        pattern="attested corpus sentence",substitutions=[],rules=[]))

def generation_gate_for_sentence(sentence,review_path="config/morphology_review.yaml"):
    """Require whole-lemma approval or an exact reviewed FEATS+form cell."""
    return check_tokens(sentence.tokens,review_path)

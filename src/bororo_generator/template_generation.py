"""Conservative generation from an attested template.

Only a token whose lemma is explicitly supported by a reviewed compositional
realizer may be changed. The attested dependency structure is preserved.
"""
from .candidate import Candidate
from .provenance import Provenance
from .compositional import realize_ako
from .orthography import normalize_bororo

def _render(tokens):
    # Conservative plain rendering; provenance retains token structure.
    return normalize_bororo(" ".join(str(t.get("form") or "") for t in tokens).strip())

def replace_ako_cell(sentence, token_id, features, source_version=None, review_path="config/morphology_review.yaml"):
    tokens=[dict(t) for t in sentence.tokens if isinstance(t.get("id"),int)]
    target=next((t for t in tokens if t.get("id")==token_id),None)
    if target is None:
        raise ValueError("target token not found")
    if str(target.get("lemma") or "")!="ako":
        raise ValueError("target lemma is not ako")

    form=realize_ako(review_path=review_path,**features)
    if form is None:
        return None

    old=str(target.get("form") or "")
    target["form"]=form
    labels=[f"{k}={v}" for k,v in sorted(features.items()) if v is not None]
    return Candidate(_render(tokens),Provenance(
        status="generated",
        source_version=source_version,
        source_sent_ids=[sentence.sent_id],
        pattern="attested UD template with reviewed ako morphology",
        substitutions=[{
            "token_id":token_id,
            "lemma":"ako",
            "old_form":old,
            "new_form":form,
            "requested_features":dict(features),
        }],
        rules=[
            "preserve_attested_dependency_structure",
            "replace_only_reviewed_ako_cell",
            "human_reviewed_morphology",
        ],
        notes=[
            "Experimental sentence candidate; not an attested CorBo sentence.",
            "Morphological realization is reviewed; sentence-level grammaticality is not asserted.",
            "requested features: "+", ".join(labels),
        ],
    ))

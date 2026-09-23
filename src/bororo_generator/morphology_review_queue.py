"""Evidence-first queue for reviewing corpus-observed forms.

Observed forms are ranked for human review.  No person value, segmentation,
stem class, or coding frame is inferred from corpus shape or frequency.
"""
from .corpus_evidence import corpus_lemma_forms
from .person_index import REVIEWED_PERSON_CELLS, reviewed_stem_class
from .context_audit import audit_lemma_contexts

def morphology_review_queue(lemmas, corpus_path):
    rows=[]
    for lemma in lemmas:
        exact=set(REVIEWED_PERSON_CELLS.get(lemma,{}).values())
        full=reviewed_stem_class(lemma)
        for obs in corpus_lemma_forms(lemma,corpus_path):
            # A full reviewed class is already generative; corpus forms still
            # remain observations, but are not queued as missing morphology.
            if full is not None:
                state="full_class_reviewed"
            elif obs["form"] in exact:
                state="exact_cell_reviewed"
            else:
                state="needs_human_review"
            rows.append({
                "lemma":lemma,
                "form":obs["form"],
                "tokens":obs["count"],
                "sent_ids":obs["sent_ids"],
                "upos":obs["upos"],
                "deprels":obs["deprels"],
                "review_state":state,
                "inferred_person":None,
                "inferred_segmentation":None,
                "inferred_stem_class":None,
                "licenses_generation":state in {"full_class_reviewed","exact_cell_reviewed"},
            })
    rank={"needs_human_review":0,"exact_cell_reviewed":1,"full_class_reviewed":2}
    return sorted(rows,key=lambda r:(rank[r["review_state"]],-r["tokens"],r["lemma"],r["form"]))


def review_packet(lemma, form, corpus_path, limit=12):
    """Return corpus contexts for one queued form without adding an analysis."""
    contexts=audit_lemma_contexts(corpus_path,lemma,limit=limit,form=form)
    return {
        "lemma":lemma,
        "form":form,
        "contexts":contexts,
        "analysis":{
            "person":None,
            "segmentation":None,
            "stem_class":None,
            "coding_frame":None,
        },
        "licenses_generation":False,
        "instruction":"Human review required; corpus context is evidence, not an inferred analysis.",
    }


def review_queue_summary(rows):
    """Summarize review workload without converting observations into analyses."""
    unresolved=[r for r in rows if r.get("review_state")=="needs_human_review"]
    return {
        "observed_forms":len(rows),
        "needs_human_review":len(unresolved),
        "tokens_needing_review":sum(r.get("tokens",0) for r in unresolved),
        "lemmas_needing_review":len({r.get("lemma") for r in unresolved}),
        "top_unresolved":[
            {"lemma":r["lemma"],"form":r["form"],"tokens":r["tokens"]}
            for r in unresolved[:10]
        ],
    }
